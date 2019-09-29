function Map() {
    var map = undefined;
    var initialized = false;
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
            if (initialized) {
                return;
            }

            const line = vnode.attrs.line;
            const elements = vnode.attrs.elements;

            fitLine(line);
            drawLine(line);
            drawMarkers(elements);

            initialized = true;
        },
        view: function () {
            return m("#map");
        },
    };
}

const Search = {
    view: function () {
        return m(".search", [
            m(".field.has-addons", [
                m("p.control.is-expanded", [
                    m("input.input.is-family-monospace", {type: "text", placeholder: "Element ID"}),
                ]),
                m("p.control", [
                    m("a.button", "Find"),
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
                        m("td", element.coords[1]),
                    ]),
                    m("tr", [
                        m("td", "longitude"),
                        m("td", element.coords[0]),
                    ]),
                ]),
            ]),
        ]);
    },
};

const Menu = {
    view: function (vnode) {
        const selected = vnode.attrs.selected;

        return m("#menu.is-family-monospace", [
            m(Search),
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
        console.log("selected " + id);
        selectedId = id;
        console.log(elementsById[selectedId]);
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
                m(Map, {line: line, elements: elements, selectElement: selectElement}),
                m(Menu, {selected: selectedId ? elementsById[selectedId] : null}),
            ];
        },
    };
}

m.mount(document.getElementById("root"), App);
