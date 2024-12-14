document.addEventListener('DOMContentLoaded', function() {
    const songList = document.querySelector('.song-list');
    const audioPlayer = document.getElementById('main-audio-player');
    const currentlyPlayingImage = document.getElementById('currently-playing-image');
    const currentlyPlayingTitle = document.getElementById('currently-playing-title');
    const currentlyPlayingArtist = document.getElementById('currently-playing-artist');
    const playPauseButton = document.getElementById('play-pause');
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');

    let songQueue = []; // Array to store song objects
    let currentSongIndex = -1; // Index of currently playing song

    // Function to create song objects
    const createSongObject = (element) => {
      return {
        url: element.dataset.songUrl,
        title: element.dataset.songTitle,
        artist: element.dataset.songArtist,
        image: element.dataset.songImage,
      };
    };


    // Populate songQueue from song list elements
    const songElements = Array.from(songList.querySelectorAll('.song'));
    songQueue = songElements.map(createSongObject);

    // Function to play a song
    const playSong = (index) => {
        if (index >= 0 && index < songQueue.length) {
            const song = songQueue[index];
            audioPlayer.src = song.url;
            audioPlayer.play();
            currentlyPlayingImage.src = song.image;
            currentlyPlayingTitle.textContent = song.title;
            currentlyPlayingArtist.textContent = song.artist;
            currentSongIndex = index;
            updatePlayPauseButton(); //Update play/pause button accordingly
        }
    };


    // Event listener for song clicks
    songList.addEventListener('click', function(event) {
        if (event.target.closest('.song')) {
            const songElement = event.target.closest('.song');
            const index = songElements.indexOf(songElement);
            playSong(index);
        }
    });

    // Event listeners for previous and next buttons
    prevButton.addEventListener('click', () => playSong(currentSongIndex - 1));
    nextButton.addEventListener('click', () => playSong(currentSongIndex + 1));

    //Play/Pause Button
    playPauseButton.addEventListener('click', () => {
        if (audioPlayer.paused) {
            audioPlayer.play();
            updatePlayPauseButton();
        } else {
            audioPlayer.pause();
            updatePlayPauseButton();
        }
    });


    const updatePlayPauseButton = () => {
      playPauseButton.textContent = audioPlayer.paused ? 'Play' : 'Pause';
    };

    //Add error handling
    audioPlayer.addEventListener('error', (error) => {
        console.error("Audio Error:", error);
        currentlyPlayingTitle.textContent = "Error loading audio.";
    });


});