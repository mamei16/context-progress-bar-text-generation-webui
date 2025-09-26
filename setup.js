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


var notify_checkbox = document.getElementById("change_notify_checkbox").children[1].firstChild;
var chat_elem = document.getElementById("chat");


var observeDOM = (function() {
  var MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

  return function(obj, callback) {
    if (!obj || obj.nodeType !== 1) {
      return;
    }

    if (MutationObserver) {
      // define a new observer
      var mutationObserver = new MutationObserver(callback);

      // have the observer observe for changes in children
      mutationObserver.observe(obj, {childList: true, subtree: true});
      return mutationObserver;
    } else if (window.addEventListener) { // browser support fallback
      obj.addEventListener('DOMNodeInserted', callback, false);
      obj.addEventListener('DOMNodeRemoved', callback, false);
    }
  }
})();

observeDOM(chat_elem, function(m) { notify_checkbox.click() });


// If version > v3.4, adapt width of progress bar
if (document.getElementsByClassName("token-display").length > 0) {
  var progressContainer = document.querySelector('.progress-container');
  progressContainer.style.marginLeft = "33px";
  progressContainer.style.width = "95.25%";
}
