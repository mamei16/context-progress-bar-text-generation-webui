function darkModeEnabled() {
    var currentCSS = document.getElementById("highlight-css");
    return currentCSS.getAttribute("href") === "file/css/highlightjs/github-dark.min.css";
}


function getColor(percentage) {
    if (percentage == 0) return "rgba(0, 0, 0, 0)";

    const bright_colors = [
        { stop: 0, color: [0, 123, 255] },
        { stop: 25, color: [0, 255, 0] },
        { stop: 50, color: [255, 255, 0] },
        { stop: 75, color: [255, 165, 0] },
        { stop: 100, color: [255, 0, 0] }
    ];

    const muted_colors = [
        { stop: 0, color: [0, 61, 128] },       // Muted blue
        { stop: 25, color: [0, 128, 0] },       // Muted green
        { stop: 50, color: [128, 128, 0] },     // Muted yellow
        { stop: 75, color: [128, 82, 0] },      // Muted orange
        { stop: 100, color: [128, 0, 0] }       // Muted red
    ];

    const colors = darkModeEnabled()? muted_colors:bright_colors;

    let startColor, endColor, startStop, endStop;
    for (let i = 0; i < colors.length - 1; i++) {
        if (percentage >= colors[i].stop && percentage <= colors[i + 1].stop) {
            startColor = colors[i].color;
            endColor = colors[i + 1].color;
            startStop = colors[i].stop;
            endStop = colors[i + 1].stop;
            break;
        }
    }

    const ratio = (percentage - startStop) / (endStop - startStop);
    const r = Math.round(startColor[0] + ratio * (endColor[0] - startColor[0]));
    const g = Math.round(startColor[1] + ratio * (endColor[1] - startColor[1]));
    const b = Math.round(startColor[2] + ratio * (endColor[2] - startColor[2]));

    return `rgb(${r}, ${g}, ${b})`;
}


function updateProgressBar(percentage) {
    if (percentage === undefined) percentage = 0;
    progressContainer.lastPercentage = percentage;
    const progressBar = document.querySelector('.progress-bar');
    progressBar.style.width = percentage + '%';
    progressBar.style.backgroundColor = getColor(percentage);
}


function toggleDarkMode() {
  if (darkModeEnabled()) {
    var lightGray = getComputedStyle(document.body).getPropertyValue("--light-gray");
    progressContainer.style.backgroundColor = lightGray;
    progressContainer.style.outlineWidth = "0px";
  } else {
    progressContainer.style.backgroundColor = "white";
    progressContainer.style.outlineWidth = "1px";
    progressContainer.style.outlineColor = "#c5c5d2";
    progressContainer.style.outlineStyle = "solid";
  }
  updateProgressBar(progressContainer.lastPercentage);
}

const progressContainer = document.querySelector('.progress-container');
toggleDarkMode();
