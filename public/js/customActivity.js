const connection = new Postmonger.Session();
let eventDefinitionKey;
let createdData = {};
let authTokens = {};

connection.trigger("ready");
connection.trigger("requestSchema");
connection.trigger("requestTokens");
connection.trigger("requestTriggerEventDefinition");

const schema = {};
let body = {metadata:{}};

connection.on("requestedTriggerEventDefinition", function (eventDefinitionModel) {
  if (eventDefinitionModel) {
    eventDefinitionKey = eventDefinitionModel.eventDefinitionKey;
  }
});
connection.on("requestedSchema", function (response) {
  for (let item of response.schema) {
    schema[item.name] = "{{" + item.key + "}}";
  }
});

const block = document.querySelector("#custom-block");
const textArea = block.querySelector("#textarea");

connection.on("initActivity", (data) => {
  createdData = { ...createdData, ...data };
  createdData.isConfigured = false;
  body = {...body, ...JSON.parse((createdData.arguments || {execute:{body:'{}'}}).execute.body)}
  console.log(body)
  /*
  insertInputElement("namespaceField", "Nome Space(Template) Smooch", body.metadata.namespace || '', buildFieldDataListener("namespace"));
  insertInputElement("nameTemplate", "Nome (Template) Smooch", body.metadata.nametemplate || '', buildFieldDataListener("nametemplate"));
  insertInputElement("imageField", "Url da Imagem", body.metadata.image || '', buildFieldDataListener("image"));
  setMessage();
  */
  insertInputElement("idTemplate", "ID Template (Blip)", body.metadata.namespace || '', buildFieldDataListener("idtemplate"));
  insertInputElement("nameTemplate", "Nome Template (Blip)", body.metadata.nametemplate || '', buildFieldDataListener("nametemplate"));
  insertInputElement("idSubBot", "id Sub (Blip)", body.metadata.idsubbot || '', buildFieldDataListener("idsubbot"));
  insertInputElement("idFluxo", "id Fluxo (Blip)", body.metadata.idfluxo || '', buildFieldDataListener("idfluxo"));
  insertInputElement("idBloco", "id Bloco (Blip)", body.metadata.idbloco || '', buildFieldDataListener("idbloco"));
  setMessage();
});

const setMessage = () => {
  textArea.innerHTML = textArea.innerHTML.replace("{{message}}", body.message || "");
  textArea.addEventListener("focusout", function (event) {
    if (!event.target.value) {
      console.log(createdData);
      return;
    }
    body["message"] = event.target.value
  });
};

const getInAttributes = (field) => {
  for (const item of ((createdData.arguments || {}).execute || {}).inArguments || []) {
    if (item[field]) {
      substringArray = item[field].split(".");
      return substringArray[substringArray.length - 1].replace("}}", "");
    } else {
      return "";
    }
  }
};

const buildFieldDataListener = (name) => (event) => setInAttributesField(name, event.target.value);

const setInAttributesField = (field, value) => {
  body.metadata[field] = value
};

const insertInputElement = (name, label, value, eventListener) => {
  let div = document.createElement("div");
  div.classList.add("slds-form-element");
  div.appendChild(createLabel(name, label));
  div.appendChild(createInput(name, value, eventListener));
  block.insertBefore(div, textArea);
};

const createLabel = (name, label) => {
  let labelElement = document.createElement("label");
  labelElement.classList.add("slds-form-element__label");
  labelElement.textContent = label;
  labelElement.setAttribute("for", name);
  let abbrElement = document.createElement("abbr");
  abbrElement.classList.add("slds-required");
  abbrElement.setAttribute("title", "required");
  abbrElement.textContent = "*";
  labelElement.appendChild(abbrElement);
  return labelElement;
};

const createInput = (name, value, eventListener) => {
  const divInput = document.createElement("div");
  divInput.classList.add("slds-form-element__control");
  const inputElement = document.createElement("input");
  inputElement.classList.add("slds-input");
  const attributes = {
    type: "text",
    id: name,
    name,
    required: true,
    value: value || "",
    placeholder: "",
  };
  for (let key in attributes) {
    inputElement.setAttribute(key, attributes[key]);
  }
  inputElement.addEventListener("focusout", eventListener);
  divInput.appendChild(inputElement);
  return divInput;
};

connection.on("requestedTokens", onGetTokens);
function onGetTokens(tokens) {
  console.log(tokens);
  authTokens = tokens;
}

connection.on("clickedNext", () => {
  save();
});

const save = () => {
  createdData["metaData"] = createdData["metaData"] || {};
  createdData["metaData"].isConfigured = true;
  createdData["arguments"].execute.inArguments.push(schema);
  createdData.arguments.execute.body = JSON.stringify(body)
  console.log(schema, createdData.arguments.execute.body);
  connection.trigger("updateActivity", createdData);
};
