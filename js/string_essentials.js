import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

// Consistent sizing for all String Essentials nodes
const DEFAULT_NODE_WIDTH = 400;

app.registerExtension({
    name: "string.strip",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "StringStrip") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const result = onNodeCreated?.apply(this, arguments);
            if (this.size) this.size[0] = DEFAULT_NODE_WIDTH;
            return result;
        };
    }
});

app.registerExtension({
    name: "string.multireplace",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "StringMultiReplace") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const result = onNodeCreated?.apply(this, arguments);
            if (this.size) this.size[0] = DEFAULT_NODE_WIDTH;
            return result;
        };
    }
});

app.registerExtension({
    name: "string.preview",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "StringPreview") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const result = onNodeCreated?.apply(this, arguments);
            this.showValueWidget = ComfyWidgets["STRING"](this, "preview", ["STRING", { multiline: true }], app).widget;
            this.showValueWidget.inputEl.readOnly = true;
            this.showValueWidget.inputEl.style.opacity = 0.6;
            if (this.size) this.size[0] = DEFAULT_NODE_WIDTH;
            return result;
        };

        const onExecuted = nodeType.prototype.onExecuted;
        nodeType.prototype.onExecuted = function (message) {
            onExecuted?.apply(this, arguments);
            if (message?.text?.[0] !== undefined) {
                this.showValueWidget.value = message.text[0];
            } else {
                this.showValueWidget.value = "";
            }
        };

        const onConnectionsChange = nodeType.prototype.onConnectionsChange;
        nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info) {
            onConnectionsChange?.apply(this, arguments);
            if (type === 1 && !connected) {
                this.showValueWidget.value = "";
            }
        };
    }
});

app.registerExtension({
    name: "string.conditionalappend",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "StringConditionalAppend") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const result = onNodeCreated?.apply(this, arguments);
            if (this.size) this.size[0] = DEFAULT_NODE_WIDTH;
            return result;
        };
    }
});

app.registerExtension({
    name: "string.textbox",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "StringTextbox") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const result = onNodeCreated?.apply(this, arguments);
            if (this.size) this.size[0] = DEFAULT_NODE_WIDTH;
            return result;
        };
    }
});
