var chatTabLabel = document.getElementById("chat-tab");
var hiddenChatTabButton = document.getElementById("hidden-chat-tab-button");
chatTabLabel.addEventListener('click', function() {
  hiddenChatTabButton.click();
});



var chatInputContainer = document.getElementById("chat-input-container");
chatInputContainer.insertAdjacentElement("beforeend", document.querySelector('.progress-container-container'));
document.querySelector('.progress-container-container').style.marginTop = "-15px";
// Avoid dead space at the bottom of the chat tab
document.getElementById("component-1").style.marginBottom = "-80px";
