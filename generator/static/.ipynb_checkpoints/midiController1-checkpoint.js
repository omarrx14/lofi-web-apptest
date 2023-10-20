
if (navigator.requestMIDIAccess) {
    navigator.requestMIDIAccess()
        .then(onMIDISuccess, onMIDIFailure);
} else {
    console.warn("WebMIDI no es soportado en este navegador.");
}

function onMIDIFailure() {
    console.warn("No se pudo acceder a tus dispositivos MIDI.");
}

function onMIDISuccess(midiAccess) {
    var inputs = midiAccess.inputs.values();
    for (var input = inputs.next(); input && !input.done; input = inputs.next()) {
        input.value.onmidimessage = onMIDIMessage;
    }
}

function onMIDIMessage(event) {
    var note = event.data[1];
    var velocity = event.data[2];
    if (velocity > 0) {
        playNoteByMidiValue(note);  // Esta función deberás implementarla para que toque la nota correspondiente en tu piano virtual
    }
}

function onMIDIMessage(event) {
    var note = event.data[1];
    var velocity = event.data[2];
    if (velocity > 0) {
        playNoteByMidiValue(note);  // Esta función deberás implementarla para que toque la nota correspondiente en tu piano virtual
    }
}

