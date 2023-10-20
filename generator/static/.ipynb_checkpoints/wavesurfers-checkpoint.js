// Inicialización de Wavesurfer
var wavesurfer = WaveSurfer.create({
    container: '#waveform',
    waveColor: 'violet',
    progressColor: 'purple'
});

// Función para tocar una nota
function playNote(note) {
    // Aquí, necesitas la URL del archivo de audio correspondiente a la nota
    // Ajusta la ruta según tu estructura de archivos
    var audioUrl = '/static/notes_audio/' + note + '.mp3';  

    wavesurfer.load(audioUrl);
    wavesurfer.on('ready', function() {
        wavesurfer.play();
    });
}

// Eventos de clic para las teclas del piano
document.querySelectorAll('.key').forEach(function(key) {
    key.addEventListener('click', function() {
        playNote(this.id);  // Usamos el ID de la tecla como el nombre de la nota
    });
});

