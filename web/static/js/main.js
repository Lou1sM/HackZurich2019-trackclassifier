function Map() {
    var map = undefined;
    var initialized = false;
    var selectedId = undefined;
    var selectElement = undefined;

    function fitLine(line) {
        map.fitBounds([line.coords[0], line.coords[line.coords.length - 1]], {padding: 50});
    }

    function drawLine(line) {
        map.addLayer({
            'id': 'track_line',
            'type': 'line',
            'source': {
                'type': 'geojson',
                'data': {
                    'type': 'Feature',
                    'id': 'track',
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': line.coords,
                    },
                },
            },
            'layout': {
                'line-join': 'round',
                'line-cap': 'square',
            },
            'paint': {
                'line-color': '#c00',
                'line-width': 3,
                'line-opacity': 0.7,
                // 'line-blur': 3,
            },
        });
    }

    function drawMarkers(elements) {
        elements.forEach(function (element) {
            const popup = new tt.Popup({
                offset: [0, -10],
                closeButton: false,
                className: 'marker-popup is-family-monospace',
            }).setHTML(`id: <strong>${element.id}</strong>`).on("open", function () {
                selectElement(element.id);
            });

            new tt.Marker({
                element: document.getElementById(element.type).cloneNode(true),
            }).setLngLat(element.coords).setPopup(popup).addTo(map);
        });
    }

    return {
        oninit: function (vnode) {
            selectElement = vnode.attrs.selectElement;
        },
        oncreate: function () {
            tt.setProductInfo('Siemens@HackZurich', '0.0.1');
            map = tt.map({
                key: 'YfDvbejIBGGLsoXT4fx1OWIxjCr5huoQ',
                container: 'map',
                center: new tt.LngLat(9.641403229722222, 46.98026536027778),
                zoom: 11,
            }).addControl(new tt.plugins.ZoomControls({
                animate: true,
            }), 'top-left');
        },
        onupdate: function (vnode) {
            // initialize data if the case
            if (!initialized) {
                const line = vnode.attrs.line;
                const elements = vnode.attrs.elements;

                fitLine(line);
                drawLine(line);
                drawMarkers(elements);

                initialized = true;
            }

            // fly to newly selected element if the case
            const selected = vnode.attrs.selected;
            if (selected && (selected.id !== selectedId)) {
                selectedId = selected.id;
                map.flyTo({
                    center: selected.coords,
                    zoom: 13,
                });
            }
        },
        view: function () {
            return m("#map");
        },
    };
}

const Search = {
    view: function (vnode) {
        const selectElement = vnode.attrs.selectElement;

        return m("form.search", {
            onsubmit: function (e) {
                e.preventDefault();
                selectElement(e.target.id.value);
            }
        }, [
            m(".field.has-addons", [
                m("p.control.is-expanded", [
                    m("input.input.is-family-monospace", {type: "text", name: "id", placeholder: "Element ID"}),
                ]),
                m("p.control", [
                    m("button.button.input.is-family-monospace", {type: "submit"}, "Find"),
                ]),
            ]),
        ]);
    },
};

const Details = {
    view: function (vnode) {
        const element = vnode.attrs.element;
        return m(".details", [
            m("table.table.is-narrow.is-fullwidth", [
                m("tbody", [
                    m("tr.has-text-weight-bold", [
                        m("td", "id"),
                        m("td", element.id),
                    ]),
                    m("tr", [
                        m("td", "latitude"),
                        m("td", element.coords[1].toFixed(6)),
                    ]),
                    m("tr", [
                        m("td", "longitude"),
                        m("td", element.coords[0].toFixed(6)),
                    ]),
                    m("tr", [
                        m("td", "relative"),
                        m("td", `${element.relative_position.toFixed(3)} km`),
                    ]),
                    m("tr", [
                        m("td", "datasheet"),
                        m("td", {style: "word-wrap: anywhere"}, [
                            m("a", {
                                href: "http://51.136.17.19/Trackdata/" + element.pdf_file,
                                target: "_blank",
                                rel: "noopener noreferrer",
                            }, element.pdf_file),
                        ]),
                    ]),
                ]),
            ]),
            m("img", {src: "http://51.136.17.19/Trackpictures/Trackpictures_LoRes/" + element.image}),
        ]);
    },
};

const Menu = {
    view: function (vnode) {
        const selected = vnode.attrs.selected;

        return m("#menu.is-family-monospace", [
            m(Search, {selectElement: vnode.attrs.selectElement}),
            selected && m(Details, {element: selected}),
        ]);
    },
};

function App() {
    var line;
    var elements;
    var elementsById;
    var selectedId;

    function selectElement(id) {
        selectedId = id;
        m.redraw();
    }

    return {
        oninit: function () {
            m.request({
                url: "/api/track",
            }).then(function (response) {
                line = response.line;
                elements = response.elements;
                elementsById = {};
                elements.forEach(function (e) {
                    elementsById[e.id] = e;
                });
            });
        },
        view: function () {
            return [
                m(Map, {
                    line: line,
                    elements: elements,
                    selected: selectedId ? elementsById[selectedId] : null,
                    selectElement: selectElement,
                }),
                m(Menu, {
                    selected: selectedId ? elementsById[selectedId] : null,
                    selectElement: selectElement,
                }),
            ];
        },
    };
}

m.mount(document.getElementById("root"), App);
