import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

// Consistent sizing for all String Essentials nodes
const DEFAULT_NODE_SIZE = [400, 200];

app.registerExtension({
    name: "string.strip",
    async beforeRegisterNodeDef(nodeType) {
        if (nodeType.comfyClass === "StringStrip") {
            nodeType.prototype.onNodeCreated = function() {
                this.addInput("input_string", "STRING");
                this.setSize(DEFAULT_NODE_SIZE);
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
                this.setSize(DEFAULT_NODE_SIZE);
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
                this.setSize(DEFAULT_NODE_SIZE);
            };

            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function(message) {
                onExecuted?.apply(this, arguments);
                if (message?.text?.[0] !== undefined) {
                    this.showValueWidget.value = message.text[0];
                } else {
                    // Clear preview if no text received
                    this.showValueWidget.value = "";
                }
            };

            // Clear preview when input is disconnected
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                if (onConnectionsChange) {
                    onConnectionsChange.apply(this, arguments);
                }

                // If input was disconnected, clear the preview
                if (type === 1 && !connected) { // type 1 = input
                    this.showValueWidget.value = "";
                }
            };
        }
    }
});

app.registerExtension({
    name: "string.conditionalappend",
    async beforeRegisterNodeDef(nodeType) {
        if (nodeType.comfyClass === "StringConditionalAppend") {
            nodeType.prototype.onNodeCreated = function() {
                this.addInput("input_string", "STRING");
                this.setSize(DEFAULT_NODE_SIZE);
            };
        }
    }
});

app.registerExtension({
    name: "string.textbox",
    async beforeRegisterNodeDef(nodeType) {
        if (nodeType.comfyClass === "StringTextbox") {
            nodeType.prototype.onNodeCreated = function() {
                this.setSize(DEFAULT_NODE_SIZE);
            };
        }
    }
});
