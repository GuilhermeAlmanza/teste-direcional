const connection = new Postmonger.Session();
let eventDefinitionKey;
let createdData = {};
let authTokens = {};

connection.trigger("ready");
connection.trigger("requestSchema");
connection.trigger("requestTokens");
connection.trigger("requestTriggerEventDefinition");

const schema = {};

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
  insertInputElement("phoneField", "Campo de Telefone", getInAttributes("phone"), buildFieldDataListener("phone"));
  setMessage();
});

const setMessage = () => {
  console.log(createdData["metaData"].message);
  textArea.innerHTML = textArea.innerHTML.replace("{{message}}", createdData["metaData"].message || "");
  textArea.addEventListener("focusout", function (event) {
    if (!event.target.value) {
      console.log(createdData);
      return;
    }
    createdData.arguments.execute.body = JSON.stringify({ message: event.target.value });
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
  createdData["arguments"] = createdData["arguments"] || {};
  createdData["arguments"].execute = createdData["arguments"].execute || {};

  createdData["arguments"].execute.inArguments = createdData["arguments"].execute.inArguments || [];
  insertedObj = {};
  insertedObj[field] = "{{Event." + eventDefinitionKey + "." + value + "}}";
  createdData["arguments"].execute.inArguments.push(insertedObj);
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
  console.log(schema);
  connection.trigger("updateActivity", createdData);
};
