var chatTabLabel = document.getElementById("chat-tab");
var hiddenChatTabButton = document.getElementById("hidden-chat-tab-button");
chatTabLabel.addEventListener('click', function() {
  hiddenChatTabButton.click();
});



var chatInputContainer = document.getElementById("chat-input-container");
chatInputContainer.insertAdjacentElement("beforeend", document.querySelector('.progress-container-container'));
document.querySelector('.progress-container-container').style.marginTop = "-15px";
// Avoid dead space at the bottom of the chat tab
document.getElementById("chat-tab").style.marginBottom = "-80px";


// Ensure "extensions" element doesn't make parts of chat input unclickable
document.getElementById("extensions").style.zIndex = -1;


// If version > v3.4, adapt width of progress bar
if (document.getElementsByClassName("token-display").length > 0) {
  var progressContainer = document.querySelector('.progress-container');
  progressContainer.style.marginLeft = "33px";
  progressContainer.style.width = "95.25%";
}
