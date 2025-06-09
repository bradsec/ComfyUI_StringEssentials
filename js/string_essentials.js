import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
    name: "string.strip",
    async beforeRegisterNodeDef(nodeType) {
        if (nodeType.comfyClass === "StringStrip") {
            nodeType.prototype.onNodeCreated = function() {
                this.addInput("input_string", "STRING");
            };
        }
    }
});

app.registerExtension({
    name: "string.multireplace",
    async beforeRegisterNodeDef(nodeType) {
        if (nodeType.comfyClass === "StringMultiReplace") {
            nodeType.prototype.onNodeCreated = function() {
                this.addInput("input_string", "STRING");
            };
        }
    }
});

app.registerExtension({
    name: "string.preview",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeType.comfyClass === "StringPreview") {
            nodeType.prototype.onNodeCreated = function() {
                this.addInput("input_string", "STRING");
                this.showValueWidget = ComfyWidgets["STRING"](this, "preview", ["STRING", { multiline: true }], app).widget;
                this.showValueWidget.inputEl.readOnly = true;
                this.showValueWidget.inputEl.style.opacity = 0.6;
            };

            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function(message) {
                onExecuted?.apply(this, arguments);
                if (message?.text?.[0] !== undefined) {
                    this.showValueWidget.value = message.text[0];
                }
            };
        }
    }
});
