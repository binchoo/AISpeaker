audioTTS = new Audio();

function nclk(event,b,c,d){
    event.preventDefault();

    if(!audioTTS.paused){
        audioTTS.pause()
        return;
    }

    var articleTitle = document.querySelector("h2.media_end_head_headline").innerText
    var articleContent = document.querySelector("div#dic_area").innerText

    console.log(articleTitle)
    audioTTS.src = '/news/voiceaudio?textQuery='+articleTitle;
    audioTTS.play()

    audioTTS.onended = function() {
        audioTTS.src = '/news/voiceaudio?textQuery='+articleContent;
        audioTTS.play()
    };
}
asdf = function(e) {
	e.preventDefault();
}
