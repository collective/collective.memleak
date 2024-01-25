
//import { instance } from "@viz-js/viz";

var instance = require("@viz-js/viz").instance;

function showGraph(dot, id) {
    instance().then(viz => {
        const svg = viz.renderSVGElement(dot);
        document.getElementById(id).appendChild(svg);
    });
}

module.exports = { showGraph:showGraph };