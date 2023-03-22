$(document).ready(function () {
    // Pause/Play functionality
    var playButton = $('.control-play'),
    album = $('.album');

    playButton.on('click', function () {
        $('.music-player-container').toggleClass('is-playing');
    });
});