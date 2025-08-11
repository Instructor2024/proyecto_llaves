# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser


class AccessLogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    personnel = models.ForeignKey('Personnel', models.DO_NOTHING)
    environment = models.ForeignKey('Environments', models.DO_NOTHING, blank=True, null=True)
    action_type = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    success = models.IntegerField()
    fingerprint_quality = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'access_logs'


class Administrators(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField(blank=True, null=True)
    fingerprint_data = models.TextField(blank=True, null=True)
    last_fingerprint_update = models.DateTimeField(blank=True, null=True)
    failed_login_attempts = models.IntegerField()
    account_locked_until = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.email

    class Meta:
        managed = True
        db_table = 'administrators'


class AdministratorsGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    administrator = models.ForeignKey(Administrators, models.DO_NOTHING)
    group = models.ForeignKey('auth.Group', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'administrators_groups'
        unique_together = (('administrator', 'group'),)


class AdministratorsUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    administrator = models.ForeignKey(Administrators, models.DO_NOTHING)
    permission = models.ForeignKey('auth.Permission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'administrators_user_permissions'
        unique_together = (('administrator', 'permission'),)


# Estos modelos están duplicados con Django, los eliminamos
# AuthGroup, AuthPermission, DjangoContentType, DjangoMigrations, DjangoSession
# son manejados automáticamente por Django


class EnvironmentKeys(models.Model):
    id = models.BigAutoField(primary_key=True)
    environment = models.OneToOneField('Environments', models.DO_NOTHING)
    drum_number = models.IntegerField(blank=True, null=True)
    drum_slot_number = models.IntegerField(blank=True, null=True)
    key_code = models.CharField(unique=True, max_length=50)
    key_type = models.CharField(max_length=15)
    is_available = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'environment_keys'


class Environments(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    picture = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    length = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    farm_id = models.BigIntegerField()
    status = models.CharField(max_length=255)
    type_environment = models.CharField(max_length=255, blank=True, null=True)
    class_environment_id = models.BigIntegerField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'environments'

    def __str__(self):
        return f"Ambiente {self.id} - {self.name}"


class KeyAssignments(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.ForeignKey(EnvironmentKeys, models.DO_NOTHING)
    personnel = models.ForeignKey('Personnel', models.DO_NOTHING)
    schedule = models.ForeignKey('Schedules', models.DO_NOTHING, blank=True, null=True)
    assigned_at = models.DateTimeField()
    returned_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'key_assignments'


class Personnel(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    document_type = models.CharField(max_length=10)
    document_number = models.CharField(unique=True, max_length=20)
    email = models.CharField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    personnel_type = models.CharField(max_length=20)
    contract_type = models.CharField(max_length=15)
    contract_start_date = models.DateField(blank=True, null=True)
    contract_end_date = models.DateField(blank=True, null=True)
    hire_date = models.DateField()
    fingerprint_data = models.TextField(blank=True, null=True)
    last_fingerprint_update = models.DateTimeField(blank=True, null=True)
    is_active = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'personnel'


class Reports(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20)
    format = models.CharField(max_length=10)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    filters = models.JSONField(blank=True, null=True)
    file_path = models.CharField(max_length=500, blank=True, null=True)
    file_size = models.PositiveIntegerField()
    generated_by = models.ForeignKey(Administrators, models.DO_NOTHING)
    generated_at = models.DateTimeField()
    downloaded_count = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'reports'


class Schedules(models.Model):
    id = models.BigAutoField(primary_key=True)
    environment = models.ForeignKey(Environments, models.DO_NOTHING)
    primary_personnel = models.ForeignKey(Personnel, models.DO_NOTHING)
    secondary_personnel = models.ForeignKey(Personnel, models.DO_NOTHING, related_name='schedules_secondary_personnel_set', blank=True, null=True)
    weekday = models.CharField(max_length=10)
    shift_type = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'schedules'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    person_id = models.BigIntegerField()
    email = models.CharField(max_length=255, blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email or self.nickname or str(self.id)

    class Meta:
        managed = False
        db_table = 'users'


class EnvironmentInstructorPrograms(models.Model):
    id = models.BigAutoField(primary_key=True)
    instructor_program_id = models.BigIntegerField()
    environment_id = models.BigIntegerField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'environment_instructor_programs'

    def __str__(self):
        return f"Programa {self.id} - Ambiente {self.environment_id}"


class People(models.Model):
    id = models.BigAutoField(primary_key=True)
    document_type = models.CharField(max_length=255, blank=True, null=True)
    document_number = models.BigIntegerField()
    date_of_issue = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=255)
    first_last_name = models.CharField(max_length=255)
    second_last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    blood_type = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    eps_id = models.BigIntegerField()
    marital_status = models.CharField(max_length=255, blank=True, null=True)
    military_card = models.IntegerField(blank=True, null=True)
    socioeconomical_status = models.CharField(max_length=255, blank=True, null=True)
    sisben_level = models.CharField(max_length=1, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    telephone1 = models.BigIntegerField(blank=True, null=True)
    telephone2 = models.BigIntegerField(blank=True, null=True)
    telephone3 = models.BigIntegerField(blank=True, null=True)
    personal_email = models.CharField(max_length=255, blank=True, null=True)
    misena_email = models.CharField(max_length=255, blank=True, null=True)
    sena_email = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    biometric_code = models.TextField(blank=True, null=True)
    population_group_id = models.BigIntegerField()
    pension_entity_id = models.BigIntegerField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'

    def __str__(self):
        return f"{self.first_name} {self.first_last_name} - {self.document_number}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.first_last_name} {self.second_last_name or ''}".strip()

    @property
    def has_biometric(self):
        return bool(self.biometric_code and self.biometric_code.strip())
