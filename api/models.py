from django.db import models

class Nivel(models.Model):
    niv_int_id = models.AutoField(primary_key=True)
    niv_txt_nombre = models.CharField(max_length=191)

    def __str__(self):
        return self.niv_txt_nombre


class Curso(models.Model):
    cur_int_id = models.AutoField(primary_key=True)
    cur_txt_nombre = models.CharField(max_length=191)
    cur_txt_descripcion = models.CharField(max_length=191)

    def __str__(self):
        return self.cur_txt_nombre


class Rol(models.Model):
    rol_int_id = models.AutoField(primary_key=True)
    rol_txt_nombre = models.CharField(max_length=191)
    rol_txt_descripcion = models.TextField()

    def __str__(self):
        return self.rol_txt_nombre


class Usuario(models.Model):
    usu_int_id = models.AutoField(primary_key=True)
    rol_int_id = models.ForeignKey(Rol, on_delete=models.RESTRICT, db_column='rol_int_id')

    usu_txt_nombre = models.CharField(max_length=191)
    usu_txt_apellidos = models.CharField(max_length=191)
    usu_txt_email = models.EmailField(max_length=191, unique=True)
    usu_txt_password = models.CharField(max_length=191)
    usu_txt_colegio = models.CharField(max_length=191)
    usu_txt_grado = models.CharField(max_length=191)
    usu_dat_fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usu_txt_nombre} {self.usu_txt_apellidos}"


class Examen(models.Model):
    exa_int_id = models.AutoField(primary_key=True)
    exa_txt_titulo = models.CharField(max_length=191)
    cur_int_id = models.ForeignKey(Curso, on_delete=models.RESTRICT, db_column='cur_int_id')
    niv_int_id = models.ForeignKey(Nivel, on_delete=models.RESTRICT, db_column='niv_int_id')

    def __str__(self):
        return self.exa_txt_titulo


class Leccion(models.Model):
    lec_int_id = models.AutoField(primary_key=True)
    lec_txt_titulo = models.CharField(max_length=191)
    cur_int_id = models.ForeignKey(Curso, on_delete=models.RESTRICT, db_column='cur_int_id')
    niv_int_id = models.ForeignKey(Nivel, on_delete=models.RESTRICT, db_column='niv_int_id')

    def __str__(self):
        return self.lec_txt_titulo


class Pregunta(models.Model):
    pre_int_id = models.AutoField(primary_key=True)
    pre_txt_texto = models.CharField(max_length=191)
    cur_int_id = models.ForeignKey(Curso, on_delete=models.RESTRICT, db_column='cur_int_id')
    niv_int_id = models.ForeignKey(Nivel, on_delete=models.RESTRICT, db_column='niv_int_id')

    def __str__(self):
        return self.pre_txt_texto


class Respuesta(models.Model):
    res_int_id = models.AutoField(primary_key=True)
    res_txt_texto = models.CharField(max_length=191)
    res_bol_es_correcta = models.BooleanField()
    pre_int_id = models.ForeignKey(Pregunta, on_delete=models.RESTRICT, db_column='pre_int_id')

    def __str__(self):
        return self.res_txt_texto


class IntentoExamen(models.Model):
    int_int_id = models.AutoField(primary_key=True)
    usu_int_id = models.ForeignKey(Usuario, on_delete=models.RESTRICT, db_column='usu_int_id')
    exa_int_id = models.ForeignKey(Examen, on_delete=models.RESTRICT, db_column='exa_int_id')
    int_flt_puntaje = models.FloatField()
    int_dat_fecha = models.DateTimeField(auto_now_add=True)


class RespuestaUsuario(models.Model):
    run_int_id = models.AutoField(primary_key=True)
    int_int_id = models.ForeignKey(IntentoExamen, on_delete=models.RESTRICT, db_column='int_int_id')
    pre_int_id = models.ForeignKey(Pregunta, on_delete=models.RESTRICT, db_column='pre_int_id')
    res_int_id = models.ForeignKey(Respuesta, on_delete=models.RESTRICT, db_column='res_int_id')
    usu_int_id = models.ForeignKey(Usuario, on_delete=models.RESTRICT, db_column='usu_int_id')
