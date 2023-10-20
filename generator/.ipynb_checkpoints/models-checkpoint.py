from django.db import models

# Modelo Usuario
class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=100, unique=True)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)

# Modelo PreferenciasUsuario
class PreferenciasUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    genero_preferido = models.CharField(max_length=50)
    instrumentos_favoritos = models.ManyToManyField('Instrumento')
    configuracion_lofi = models.JSONField()

# Modelo Instrumento
class Instrumento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    archivo_sample = models.FileField(upload_to='samples/')
    CATEGORIAS = (
        ('percusion', 'Percusión'),
        ('cuerda', 'Cuerda'),
        ('viento', 'Viento'),
    )
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)

# Modelo Efecto
class Efecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    parametros = models.JSONField()
    archivo_sample = models.FileField(upload_to='efectos/', null=True, blank=True)

# Modelo SampleAmbiental
class SampleAmbiental(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    archivo_audio = models.FileField(upload_to='ambientales/')

# Modelo Secuencia
class Secuencia(models.Model):
    nombre = models.CharField(max_length=100)
    orden = models.TextField()
    duracion = models.DurationField()

# Modelo EstacionRadio
class EstacionRadio(models.Model):
    nombre = models.CharField(max_length=100)
    url_streaming = models.URLField()
    descripcion = models.TextField()

# Modelo Recomendacion
class Recomendacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    referencia = models.IntegerField()

# Modelo VersionMelodia
class VersionMelodia(models.Model):
    melodia = models.ForeignKey('Melodía', on_delete=models.CASCADE)
    fecha_version = models.DateTimeField(auto_now_add=True)
    archivo_midi = models.FileField(upload_to='versiones/')
    descripcion = models.TextField()

# Modelo Comentario
class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    melodia = models.ForeignKey('Melodía', on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

# Modelo Colaboracion
class Colaboracion(models.Model):
    usuario_principal = models.ForeignKey(Usuario, related_name='colaboraciones_iniciadas', on_delete=models.CASCADE)
    usuario_colaborador = models.ForeignKey(Usuario, related_name='colaboraciones_recibidas', on_delete=models.CASCADE)
    melodia = models.ForeignKey('Melodía', on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)

# Modelo GeneracionLofi
class GeneracionLofi(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    melodia_base = models.ForeignKey('Melodía', on_delete=models.CASCADE)
    configuracion = models.JSONField()
    archivo_generado = models.FileField(upload_to='generated/')
    fecha_generacion = models.DateTimeField(auto_now_add=True)

# Modelo Melodía
class Melodía(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    archivo_midi = models.FileField(upload_to='melodias/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    instrumentos_utilizados = models.ManyToManyField(Instrumento)


class Note(models.Model):
    name = models.CharField(max_length=10)  # e.g., 'A4', 'C#5'
    frequency = models.FloatField(help_text="Frequency of the note in Hz")  # e.g., 440.0 for A4
    duration = models.FloatField(help_text="Duration of the note in seconds")
    volume = models.FloatField(help_text="Intensity of the note, typically between 0 and 1")
    audio_file = models.FileField(upload_to='notes_audio/')


    def __str__(self):
        return self.name

# Model to represent a Scale
class Scale(models.Model):
    name = models.CharField(max_length=50)  # e.g., 'C Major', 'D Minor'
    notes = models.ManyToManyField(Note, related_name="scales")

    def __str__(self):
        return self.name

# Model to represent a Chord
class Chord(models.Model):
    name = models.CharField(max_length=50)  # e.g., 'C Major Chord'
    notes = models.ManyToManyField(Note, related_name="chords")
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE, related_name="chords")

    def __str__(self):
        return self.name

# Model to represent a Rhythm Pattern
class RhythmPattern(models.Model):
    name = models.CharField(max_length=100, help_text="Descriptive name of the rhythm pattern")
    duration_pattern = models.TextField(help_text="Pattern of durations, represented as a list of numbers in string format, e.g.: '[0.5, 0.25, 0.25]'")



# Model to represent a Musical Piece or Composition
class Composition(models.Model):
    title = models.CharField(max_length=200)
    composer = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="compositions")
    notes = models.ManyToManyField(Note, through='CompositionNote', related_name="compositions")
    chords = models.ManyToManyField(Chord, through='CompositionChord', related_name="compositions")
    rhythm_pattern = models.ForeignKey(RhythmPattern, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

# Intermediate model to represent a Note in a Composition
class CompositionNote(models.Model):
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    start_time = models.FloatField(help_text="Start time of the note in the composition, in seconds")
    end_time = models.FloatField(help_text="End time of the note in the composition, in seconds")

# Intermediate model to represent a Chord in a Composition
class CompositionChord(models.Model):
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    chord = models.ForeignKey(Chord, on_delete=models.CASCADE)
    start_time = models.FloatField(help_text="Start time of the chord in the composition, in seconds")
    end_time = models.FloatField(help_text="End time of the chord in the composition, in seconds")

class MusicFeature(models.Model):
    composition = models.OneToOneField(Composition, on_delete=models.CASCADE)
    spectrogram = models.FileField(upload_to='features/')
    tempo = models.FloatField()
    key_signature = models.CharField(max_length=50)
    time_signature = models.CharField(max_length=10)
    harmonic_progression = models.TextField()

class GenerationHistory(models.Model):
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    date_generated = models.DateTimeField(auto_now_add=True)
    algorithm_used = models.CharField(max_length=200)
    user_feedback = models.PositiveIntegerField(help_text="Rating given by user, e.g., from 1 to 5")
    other_metrics = models.JSONField()

class FeatureVector(models.Model):
    composition = models.OneToOneField(Composition, on_delete=models.CASCADE)
    vector = models.JSONField(help_text="Numeric representation of music features")

class DimensionalityReduction(models.Model):
    original_vector = models.ForeignKey(FeatureVector, on_delete=models.CASCADE)
    reduced_vector = models.JSONField(help_text="Reduced dimension representation")
    method_used = models.CharField(max_length=100)  # e.g., "PCA", "t-SNE"

class MusicCluster(models.Model):
    composition = models.OneToOneField(Composition, on_delete=models.CASCADE)
    cluster_id = models.PositiveIntegerField()

class AutoencoderModel(models.Model):
    name = models.CharField(max_length=200)
    model_file = models.FileField(upload_to='autoencoders/')
    date_trained = models.DateTimeField(auto_now_add=True)

class ExperimentHistory(models.Model):
    date_conducted = models.DateTimeField(auto_now_add=True)
    algorithm_used = models.CharField(max_length=200)
    parameters = models.JSONField()
    metrics = models.JSONField()
    notes = models.TextField(null=True, blank=True)

    
    
    # Create your models here.
class Song(models.Model):
    title = models.TextField()
    artist = models.TextField()
    image = models.ImageField(blank=True, null=True)  # Permitir que la imagen sea opcional
    audio_file = models.FileField(blank=True, null=True)
    audio_link = models.CharField(max_length=200, blank=True, null=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)  # Nuevo campo para archivos de video
    video_link = models.URLField(blank=True, null=True)  # Nuevo campo para enlaces de video
    duration = models.CharField(max_length=20)
    paginate_by = 2

    def __str__(self):
        return self.title

    
class Sound(models.Model):
    name = models.CharField(max_length=200)
    pattern = models.BinaryField()  # Representará el patrón de activación. Podrías querer usar otro campo.


class Channel(models.Model):
    name = models.CharField(max_length=200)
    grid = models.CharField(max_length=100)  # Esto puede almacenar una cadena como '10100101' para representar el patrón
