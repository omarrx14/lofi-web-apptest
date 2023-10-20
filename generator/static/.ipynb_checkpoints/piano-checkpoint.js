document.addEventListener('DOMContentLoaded', function() {
    // Inicialización de Wavesurfer
    var wavesurfer = WaveSurfer.create({
        container: '#waveform',
        waveColor: getRandomColor(),
        progressColor: getRandomColor()
    });

    // Función para generar un color aleatorio en formato hexadecimal
    function getRandomColor() {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    // Función para tocar una nota usando Wavesurfer
function playNote(noteElement) {
    var noteId = noteElement.id;
    var audioUrlMp3 = '/static/notes_audio/' + noteId + '.mp3';
    var audioUrlWav = '/static/notes_audio/' + noteId + '.wav';

    // Generar un nuevo color aleatorio y aplicarlo a la waveform y a la nota
    var newColor = getRandomColor();
    wavesurfer.setWaveColor(newColor);
    noteElement.style.backgroundColor = newColor;

    // Intenta cargar el archivo .mp3
    wavesurfer.load(audioUrlMp3);

    wavesurfer.on('ready', function() {
        wavesurfer.play();
        // Limpiar los eventos para evitar la iteración infinita
        wavesurfer.un('ready');
        wavesurfer.un('error');
    });

    wavesurfer.on('error', function() {
        // Si hay un error con el archivo .mp3, intenta cargar el archivo .wav
        wavesurfer.load(audioUrlWav);
        // Limpiar el evento de error para evitar la iteración infinita
        wavesurfer.un('error');
        wavesurfer.on('ready', function() {
            wavesurfer.play();
            // Limpiar el evento de ready para evitar la iteración infinita
            wavesurfer.un('ready');
        });
    });
}


    // Eventos de clic para las teclas del piano
    document.querySelectorAll('.key').forEach(function(key) {
        key.addEventListener('click', function() {
            playNote(this);  // Pasamos el elemento tecla a la función
        });
    });

    // Función para manejar mensajes MIDI
    function onMIDIMessage(message) {
        var command = message.data[0];
        var note = message.data[1];
        var velocity = (message.data.length > 2) ? message.data[2] : 0; 

        // Mapeo de notas MIDI a notas del piano virtual
        var noteMap = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
        var octave = Math.floor(note / 12);
        var keyNote = noteMap[note % 12] + octave;

        if (command === 144 && velocity > 0) { 
            var noteElement = document.getElementById(keyNote);
            if(noteElement) {
                playNote(noteElement);
            }
        }
    }

    // Función para solicitar acceso a MIDI y conectar el teclado
    function enableMIDI() {
        if (navigator.requestMIDIAccess) {
            navigator.requestMIDIAccess({sysex: false}).then(onMIDISuccess, onMIDIFailure);
        } else {
            console.warn("No se pudo acceder a la API MIDI.");
        }
    }

    // Función que se ejecuta si se obtiene acceso a MIDI
    function onMIDISuccess(midiAccess) {
        var inputs = midiAccess.inputs.values();
        for (var input = inputs.next(); input && !input.done; input = inputs.next()) {
            input.value.onmidimessage = onMIDIMessage;
        }
    }

    // Función que se ejecuta si falla el acceso a MIDI
    function onMIDIFailure() {
        console.error("No se pudo acceder a los dispositivos MIDI.");
    }

    // Habilitar MIDI al cargar la página
    enableMIDI();
});


