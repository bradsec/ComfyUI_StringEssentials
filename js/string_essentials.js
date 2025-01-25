import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "string.strip",
    async beforeRegisterNodeDef(nodeType) {
        if (nodeType.comfyClass === "StringStrip") {
            nodeType.prototype.onNodeCreated = function() {
                // Add an input port for `input_text`
                this.addInput("input_string", "STRING");
            };
        }
    }
});

app.registerExtension({
    name: "string.replace",
    async beforeRegisterNodeDef(nodeType) {
        if (nodeType.comfyClass === "StringReplace") {
            nodeType.prototype.onNodeCreated = function() {
                // Add an input port for `input_text`
                this.addInput("input_string", "STRING");
            };
        }
    }
});