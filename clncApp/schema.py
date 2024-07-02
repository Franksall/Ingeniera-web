# Importa los módulos necesarios de graphene y graphene_django
import graphene
from graphene_django import DjangoObjectType
from mainapp.models import Doctor, Nurse, Patient, InsuranceAccount, Appointment, Consultation, Bill, Prescription,Address,CommonInfo,InsuranceAgency



# Define un tipo de objeto para la dirección
class AddressType(DjangoObjectType):
    class Meta:
        model = Address

# Define un tipo de objeto común para la información de personas (abstracto)
class CommonInfoType(DjangoObjectType):
    class Meta:
        model = CommonInfo
        exclude_fields = ('objects',)  # Excluye el campo 'objects'

# Define un tipo de objeto para los doctores
class DoctorType(DjangoObjectType):
    class Meta:
        model = Doctor

# Define un tipo de objeto para las enfermeras
class NurseType(DjangoObjectType):
    class Meta:
        model = Nurse

# Define un tipo de objeto para los pacientes
class PatientType(DjangoObjectType):
    class Meta:
        model = Patient

# Define un tipo de objeto para la cuenta de seguro
class InsuranceAccountType(DjangoObjectType):
    class Meta:
        model = InsuranceAccount

# Define un tipo de objeto para las citas
class AppointmentType(DjangoObjectType):
    class Meta:
        model = Appointment

# Define un tipo de objeto para las consultas
class ConsultationType(DjangoObjectType):
    class Meta:
        model = Consultation

# Define un tipo de objeto para las facturas
class BillType(DjangoObjectType):
    class Meta:
        model = Bill

# Define un tipo de objeto para las prescripciones
class PrescriptionType(DjangoObjectType):
    class Meta:
        model = Prescription

# Define un tipo de objeto para la dirección
class InsuranceAgencyType(DjangoObjectType):
    class Meta:
        model = InsuranceAgency


# Define una consulta para obtener todos los doctores
class Query(graphene.ObjectType):
    # Resolver para obtener todos los doctores
    all_doctors = graphene.List(DoctorType)

    def resolve_all_doctors(self, info, **kwargs):
        return Doctor.objects.all()

    # Resolver para obtener todas las enfermeras
    all_nurses = graphene.List(NurseType)

    def resolve_all_nurses(self, info, **kwargs):
        return Nurse.objects.all()

    # Resolver para obtener todos los pacientes
    all_patients = graphene.List(PatientType)

    def resolve_all_patients(self, info, **kwargs):
        return Patient.objects.all()

    # Resolver para obtener todas las cuentas de seguro
    all_insurance_accounts = graphene.List(InsuranceAccountType)

    def resolve_all_insurance_accounts(self, info, **kwargs):
        return InsuranceAccount.objects.all()

    # Resolver para obtener todas las citas
    all_appointments = graphene.List(AppointmentType)

    def resolve_all_appointments(self, info, **kwargs):
        return Appointment.objects.all()

    # Resolver para obtener todas las consultas
    all_consultations = graphene.List(ConsultationType)

    def resolve_all_consultations(self, info, **kwargs):
        return Consultation.objects.all()

    # Resolver para obtener todas las facturas
    all_bills = graphene.List(BillType)

    def resolve_all_bills(self, info, **kwargs):
        return Bill.objects.all()

    # Resolver para obtener todas las prescripciones
    all_prescriptions = graphene.List(PrescriptionType)

    def resolve_all_prescriptions(self, info, **kwargs):
        return Prescription.objects.all()

    # Resolver para obtener todas las direcciones
    all_addresses = graphene.List(AddressType)

    def resolve_all_addresses(self, info, **kwargs):
        return Address.objects.all()

    # Resolver para obtener toda la información común
    all_common_info = graphene.List(CommonInfoType)

    def resolve_all_common_info(self, info, **kwargs):
        return CommonInfo.objects.all()
     # Resolver para obtener toda la información común
    all_Insurance_Agency = graphene.List(InsuranceAgencyType)

    def resolve_all_Insurance_Agency(self, info, **kwargs):
        return CommonInfo.objects.all()


# Define una mutación para crear un nuevo doctor
class CreateDoctorMutation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        birth_date = graphene.Date()
        sex = graphene.String()
        cin = graphene.String()
        phone_nb = graphene.String()
        address_id = graphene.Int()
        email = graphene.String()
        pwd = graphene.String()
        salary = graphene.Float()
        specialty = graphene.String()
        is_active = graphene.Boolean()

    doctor = graphene.Field(DoctorType)

    def mutate(self, info, first_name=None, last_name=None, birth_date=None, sex=None, cin=None, phone_nb=None, address_id=None, email=None, pwd=None, salary=None, specialty=None, is_active=True):
        if sex and sex not in ['Male', 'Female']:
            raise Exception("Invalid value for sex. Use 'Male' or 'Female'.")
        
        if specialty and specialty not in ['General practice', 'Clinical radiology', 'Anaesthesia', 'Ophthalmology']:
            raise Exception("Invalid value for specialty.")

        address = Address.objects.get(pk=address_id) if address_id else None
        doctor = Doctor(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            sex=sex,
            cin=cin,
            phone_nb=phone_nb,
            address=address,
            email=email,
            pwd=pwd,
            salary=salary,
            specialty=specialty,
            is_active=is_active
        )
        doctor.save()
        return CreateDoctorMutation(doctor=doctor)
# Define una mutación para actualizar un doctor existente
class UpdateDoctorMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        birth_date = graphene.Date()
        sex = graphene.String()
        cin = graphene.String()
        phone_nb = graphene.String()
        address_id = graphene.Int()
        salary = graphene.String()

    doctor = graphene.Field(DoctorType)

    def mutate(self, info, id, **kwargs):
        doctor = Doctor.objects.get(pk=id)

        # Actualizar los campos solo si se proporcionan
        if 'first_name' in kwargs:
            doctor.first_name = kwargs['first_name']
        if 'last_name' in kwargs:
            doctor.last_name = kwargs['last_name']
        if 'birth_date' in kwargs:
            doctor.birth_date = kwargs['birth_date']
        if 'sex' in kwargs:
            doctor.sex = kwargs['sex']
        if 'cin' in kwargs:
            doctor.cin = kwargs['cin']
        if 'phone_nb' in kwargs:
            doctor.phone_nb = kwargs['phone_nb']
        if 'address_id' in kwargs:
            address = Address.objects.get(pk=kwargs['address_id'])
            doctor.address = address
        if 'salary' in kwargs:
            doctor.salary = kwargs['salary']

        doctor.save()
        return UpdateDoctorMutation(doctor=doctor)


# Define una mutación para eliminar un doctor
class DeleteDoctorMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    message = graphene.String()

    def mutate(self, info, id):
        doctor = Doctor.objects.get(pk=id)
        doctor.delete()
        return DeleteDoctorMutation(message=f"Doctor ha sido  {id} DESPEDIDO")


# Mutación para crear una nueva enfermera
class CreateNurseMutation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        birth_date = graphene.Date()
        sex = graphene.String()
        cin = graphene.String()
        phone_nb = graphene.String()
        address_id = graphene.Int()

    nurse = graphene.Field(NurseType)

    def mutate(self, info, first_name, last_name, birth_date, sex, cin, phone_nb, address_id):
        address = Address.objects.get(pk=address_id)
        nurse = Nurse(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            sex=sex,
            cin=cin,
            phone_nb=phone_nb,
            address=address
        )
        nurse.save()
        return CreateNurseMutation(nurse=nurse)

# Mutación para actualizar una enfermera existente
class UpdateNurseMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        first_name = graphene.String()
        last_name = graphene.String()
        birth_date = graphene.Date()
        sex = graphene.String()
        cin = graphene.String()
        phone_nb = graphene.String()
        address_id = graphene.Int()

    nurse = graphene.Field(NurseType)

    def mutate(self, info, id, first_name, last_name, birth_date, sex, cin, phone_nb, address_id):
        nurse = Nurse.objects.get(pk=id)
        address = Address.objects.get(pk=address_id)
        nurse.first_name = first_name
        nurse.last_name = last_name
        nurse.birth_date = birth_date
        nurse.sex = sex
        nurse.cin = cin
        nurse.phone_nb = phone_nb
        nurse.address = address
        nurse.save()
        return UpdateNurseMutation(nurse=nurse)

# Mutación para eliminar una enfermera
class DeleteNurseMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    message = graphene.String()

    def mutate(self, info, id):
        nurse = Nurse.objects.get(pk=id)
        nurse.delete()
        return DeleteNurseMutation(message=f"Enfermera ha sido  {id} DESPEDIDA")

# Agregar las mutaciones de enfermera al esquema de mutaciones
class Mutation(graphene.ObjectType):
    create_doctor = CreateDoctorMutation.Field()
    update_doctor = UpdateDoctorMutation.Field()
    delete_doctor = DeleteDoctorMutation.Field()

    create_nurse = CreateNurseMutation.Field()
    update_nurse = UpdateNurseMutation.Field()
    delete_nurse = DeleteNurseMutation.Field()
# Mutación para crear un nuevo paciente
class CreatePatientMutation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        birth_date = graphene.Date()
        sex = graphene.String()
        cin = graphene.String()
        phone_nb = graphene.String()
        address_id = graphene.Int()

    patient = graphene.Field(PatientType)

    def mutate(self, info, first_name, last_name, birth_date, sex, cin, phone_nb, address_id):
        address = Address.objects.get(pk=address_id)
        patient = Patient(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            sex=sex,
            cin=cin,
            phone_nb=phone_nb,
            address=address
        )
        patient.save()
        return CreatePatientMutation(patient=patient)

# Mutación para actualizar un paciente existente
class UpdatePatientMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        first_name = graphene.String()
        last_name = graphene.String()
        birth_date = graphene.Date()
        sex = graphene.String()
        cin = graphene.String()
        phone_nb = graphene.String()
        address_id = graphene.Int()

    patient = graphene.Field(PatientType)

    def mutate(self, info, id, first_name, last_name, birth_date, sex, cin, phone_nb, address_id):
        patient = Patient.objects.get(pk=id)
        address = Address.objects.get(pk=address_id)
        patient.first_name = first_name
        patient.last_name = last_name
        patient.birth_date = birth_date
        patient.sex = sex
        patient.cin = cin
        patient.phone_nb = phone_nb
        patient.address = address
        patient.save()
        return UpdatePatientMutation(patient=patient)

# Mutación para eliminar un paciente
class DeletePatientMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    message = graphene.String()

    def mutate(self, info, id):
        patient = Patient.objects.get(pk=id)
        patient.delete()
        return DeletePatientMutation(message=f"Paciente con id:  {id} ha Muerto")
# Mutación para crear una nueva cuenta de seguro
class CreateInsuranceAccountMutation(graphene.Mutation):
    class Arguments:
        patient_id = graphene.Int()
        insurance_agency_id = graphene.Int()
        policy_number = graphene.String()
        valid_from = graphene.Date()
        valid_to = graphene.Date()

    insurance_account = graphene.Field(InsuranceAccountType)

    def mutate(self, info, patient_id, insurance_agency_id, policy_number, valid_from, valid_to):
        patient = Patient.objects.get(pk=patient_id)
        insurance_agency = InsuranceAgency.objects.get(pk=insurance_agency_id)
        insurance_account = InsuranceAccount(
            patient=patient,
            insurance_agency=insurance_agency,
            policy_number=policy_number,
            valid_from=valid_from,
            valid_to=valid_to
        )
        insurance_account.save()
        return CreateInsuranceAccountMutation(insurance_account=insurance_account)

# Mutación para actualizar una cuenta de seguro existente
class UpdateInsuranceAccountMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        patient_id = graphene.Int()
        insurance_agency_id = graphene.Int()
        policy_number = graphene.String()
        valid_from = graphene.Date()
        valid_to = graphene.Date()

    insurance_account = graphene.Field(InsuranceAccountType)

    def mutate(self, info, id, patient_id, insurance_agency_id, policy_number, valid_from, valid_to):
        insurance_account = InsuranceAccount.objects.get(pk=id)
        patient = Patient.objects.get(pk=patient_id)
        insurance_agency = InsuranceAgency.objects.get(pk=insurance_agency_id)
        insurance_account.patient = patient
        insurance_account.insurance_agency = insurance_agency
        insurance_account.policy_number = policy_number
        insurance_account.valid_from = valid_from
        insurance_account.valid_to = valid_to
        insurance_account.save()
        return UpdateInsuranceAccountMutation(insurance_account=insurance_account)

# Mutación para eliminar una cuenta de seguro
class DeleteInsuranceAccountMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    message = graphene.String()

    def mutate(self, info, id):
        insurance_account = InsuranceAccount.objects.get(pk=id)
        insurance_account.delete()
        return DeleteInsuranceAccountMutation(message=f"Insurance Account with id {id} deleted")
# Mutación para crear una nueva cita
class CreateAppointmentMutation(graphene.Mutation):
    class Arguments:
        patient_id = graphene.Int()
        doctor_id = graphene.Int()
        appointment_date = graphene.Date()
        reason = graphene.String()

    appointment = graphene.Field(AppointmentType)

    def mutate(self, info, patient_id, doctor_id, appointment_date, reason):
        patient = Patient.objects.get(pk=patient_id)
        doctor = Doctor.objects.get(pk=doctor_id)
        appointment = Appointment(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            reason=reason
        )
        appointment.save()
        return CreateAppointmentMutation(appointment=appointment)

# Mutación para actualizar una cita existente
class UpdateAppointmentMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        patient_id = graphene.Int()
        doctor_id = graphene.Int()
        appointment_date = graphene.Date()
        reason = graphene.String()

    appointment = graphene.Field(AppointmentType)

    def mutate(self, info, id, patient_id, doctor_id, appointment_date, reason):
        appointment = Appointment.objects.get(pk=id)
        patient = Patient.objects.get(pk=patient_id)
        doctor = Doctor.objects.get(pk=doctor_id)
        appointment.patient = patient
        appointment.doctor = doctor
        appointment.appointment_date = appointment_date
        appointment.reason = reason
        appointment.save()
        return UpdateAppointmentMutation(appointment=appointment)

# Mutación para eliminar una cita
class DeleteAppointmentMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    message = graphene.String()

    def mutate(self, info, id):
        appointment = Appointment.objects.get(pk=id)
        appointment.delete()
        return DeleteAppointmentMutation(message=f"Appointment with id {id} deleted")
# Mutación para crear una nueva consulta
class CreateConsultationMutation(graphene.Mutation):
    class Arguments:
        patient_id = graphene.Int()
        doctor_id = graphene.Int()
        consultation_date = graphene.Date()
        symptoms = graphene.String()
        diagnosis = graphene.String()
        treatment = graphene.String()

    consultation = graphene.Field(ConsultationType)

    def mutate(self, info, patient_id, doctor_id, consultation_date, symptoms, diagnosis, treatment):
        patient = Patient.objects.get(pk=patient_id)
        doctor = Doctor.objects.get(pk=doctor_id)
        consultation = Consultation(
            patient=patient,
            doctor=doctor,
            consultation_date=consultation_date,
            symptoms=symptoms,
            diagnosis=diagnosis,
            treatment=treatment
        )
        consultation.save()
        return CreateConsultationMutation(consultation=consultation)

# Mutación para actualizar una consulta existente
class UpdateConsultationMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        patient_id = graphene.Int()
        doctor_id = graphene.Int()
        consultation_date = graphene.Date()
        symptoms = graphene.String()
        diagnosis = graphene.String()
        treatment = graphene.String()

    consultation = graphene.Field(ConsultationType)

    def mutate(self, info, id, patient_id, doctor_id, consultation_date, symptoms, diagnosis, treatment):
        consultation = Consultation.objects.get(pk=id)
        patient = Patient.objects.get(pk=patient_id)
        doctor = Doctor.objects.get(pk=doctor_id)
        consultation.patient = patient
        consultation.doctor = doctor
        consultation.consultation_date = consultation_date
        consultation.symptoms = symptoms
        consultation.diagnosis = diagnosis
        consultation.treatment = treatment
        consultation.save()
        return UpdateConsultationMutation(consultation=consultation)

# Mutación para eliminar una consulta
class DeleteConsultationMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    message = graphene.String()

    def mutate(self, info, id):
        consultation = Consultation.objects.get(pk=id)
        consultation.delete()
        return DeleteConsultationMutation(message=f"Consultation with id {id} deleted")
# Mutación para crear una nueva factura
class CreateBillMutation(graphene.Mutation):
    class Arguments:
        patient_id = graphene.Int()
        amount = graphene.Float()
        due_date = graphene.Date()
        paid = graphene.Boolean()

    bill = graphene.Field(BillType)

    def mutate(self, info, patient_id, amount, due_date, paid):
        patient = Patient.objects.get(pk=patient_id)
        bill = Bill(
            patient=patient,
            amount=amount,
            due_date=due_date,
            paid=paid
        )
        bill.save()
        return CreateBillMutation(bill=bill)

# Mutación para actualizar una factura existente
class UpdateBillMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        patient_id = graphene.Int()
        amount = graphene.Float()
        due_date = graphene.Date()
        paid = graphene.Boolean()

    bill = graphene.Field(BillType)

    def mutate(self, info, id, patient_id, amount, due_date, paid):
        bill = Bill.objects.get(pk=id)
        patient = Patient.objects.get(pk=patient_id)
        bill.patient = patient
        bill.amount = amount
        bill.due_date = due_date
        bill.paid = paid
        bill.save()
        return UpdateBillMutation(bill=bill)

# Mutación para eliminar una factura
class DeleteBillMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    message = graphene.String()

    def mutate(self, info, id):
        bill = Bill.objects.get(pk=id)
        bill.delete()
        return DeleteBillMutation(message=f"Bill with id {id} deleted")
# Mutación para crear una nueva prescripción
class CreatePrescriptionMutation(graphene.Mutation):
    class Arguments:
        patient_id = graphene.Int()
        doctor_id = graphene.Int()
        prescription_date = graphene.Date()
        medication = graphene.String()
        instructions = graphene.String()

    prescription = graphene.Field(PrescriptionType)

    def mutate(self, info, patient_id, doctor_id, prescription_date, medication, instructions):
        patient = Patient.objects.get(pk=patient_id)
        doctor = Doctor.objects.get(pk=doctor_id)
        prescription = Prescription(
            patient=patient,
            doctor=doctor,
            prescription_date=prescription_date,
            medication=medication,
            instructions=instructions
        )
        prescription.save()
        return CreatePrescriptionMutation(prescription=prescription)

# Mutación para actualizar una prescripción existente
class UpdatePrescriptionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        patient_id = graphene.Int()
        doctor_id = graphene.Int()
        prescription_date = graphene.Date()
        medication = graphene.String()
        instructions = graphene.String()

    prescription = graphene.Field(PrescriptionType)

    def mutate(self, info, id, patient_id, doctor_id, prescription_date, medication, instructions):
        prescription = Prescription.objects.get(pk=id)
        patient = Patient.objects.get(pk=patient_id)
        doctor = Doctor.objects.get(pk=doctor_id)
        prescription.patient = patient
        prescription.doctor = doctor
        prescription.prescription_date = prescription_date
        prescription.medication = medication
        prescription.instructions = instructions
        prescription.save()
        return UpdatePrescriptionMutation(prescription=prescription)

# Mutación para eliminar una prescripción
class DeletePrescriptionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    message = graphene.String()

    def mutate(self, info, id):
        prescription = Prescription.objects.get(pk=id)
        prescription.delete()
        return DeletePrescriptionMutation(message=f"Prescription with id {id} deleted")
# Mutación para crear una nueva dirección
class CreateAddressMutation(graphene.Mutation):
    class Arguments:
        street = graphene.String()
        city = graphene.String()
        state = graphene.String()
        zip_code = graphene.String()

    address = graphene.Field(AddressType)

    def mutate(self, info, street, city, state, zip_code):
        address = Address(
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        address.save()
        return CreateAddressMutation(address=address)

# Mutación para actualizar una dirección existente
class UpdateAddressMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        street = graphene.String()
        city = graphene.String()
        state = graphene.String()
        zip_code = graphene.String()

    address = graphene.Field(AddressType)

    def mutate(self, info, id, street, city, state, zip_code):
        address = Address.objects.get(pk=id)
        address.street = street
        address.city = city
        address.state = state
        address.zip_code = zip_code
        address.save()
        return UpdateAddressMutation(address=address)

# Mutación para eliminar una dirección
class DeleteAddressMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    message = graphene.String()

    def mutate(self, info, id):
        address = Address.objects.get(pk=id)
        address.delete()
        return DeleteAddressMutation(message=f"Address with id {id} deleted")
# Mutación para crear nueva información común
class CreateCommonInfoMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    common_info = graphene.Field(CommonInfoType)

    def mutate(self, info, name, description):
        common_info = CommonInfo(
            name=name,
            description=description
        )
        common_info.save()
        return CreateCommonInfoMutation(common_info=common_info)

# Mutación para actualizar información común existente
class UpdateCommonInfoMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        description = graphene.String()

    common_info = graphene.Field(CommonInfoType)

    def mutate(self, info, id, name, description):
        common_info = CommonInfo.objects.get(pk=id)
        common_info.name = name
        common_info.description = description
        common_info.save()
        return UpdateCommonInfoMutation(common_info=common_info)

# Mutación para eliminar información común
class DeleteCommonInfoMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    message = graphene.String()

    def mutate(self, info, id):
        common_info = CommonInfo.objects.get(pk=id)
        common_info.delete()
        return DeleteCommonInfoMutation(message=f"CommonInfo with id {id} deleted")
#saasassainsranceagenr   
class CreateInsuranceAgencyMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        address_id = graphene.Int()

    insurance_agency = graphene.Field(InsuranceAgencyType)

    def mutate(self, info, name, address_id):
        address = Address.objects.get(pk=address_id)
        insurance_agency = InsuranceAgency(
            name=name,
            address=address
        )
        insurance_agency.save()
        return CreateInsuranceAgencyMutation(insurance_agency=insurance_agency)

# Mutación para actualizar una agencia de seguros existente
class UpdateInsuranceAgencyMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        address_id = graphene.Int()

    insurance_agency = graphene.Field(InsuranceAgencyType)

    def mutate(self, info, id, name, address_id):
        insurance_agency = InsuranceAgency.objects.get(pk=id)
        address = Address.objects.get(pk=address_id)
        insurance_agency.name = name
        insurance_agency.address = address
        insurance_agency.save()
        return UpdateInsuranceAgencyMutation(insurance_agency=insurance_agency)

# Mutación para eliminar una agencia de seguros
class DeleteInsuranceAgencyMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    message = graphene.String()

    def mutate(self, info, id):
        insurance_agency = InsuranceAgency.objects.get(pk=id)
        insurance_agency.delete()
        return DeleteInsuranceAgencyMutation(message=f"InsuranceAgency with id {id} deleted")

# Define el esquema de GraphQL con la consulta y las mutaciones definidas
class Mutation(graphene.ObjectType):
    create_doctor = CreateDoctorMutation.Field()
    update_doctor = UpdateDoctorMutation.Field()
    delete_doctor = DeleteDoctorMutation.Field()

    create_nurse = CreateNurseMutation.Field()
    update_nurse = UpdateNurseMutation.Field()
    delete_nurse = DeleteNurseMutation.Field()

    create_patient = CreatePatientMutation.Field()
    update_patient = UpdatePatientMutation.Field()
    delete_patient = DeletePatientMutation.Field()

    create_insurance_account = CreateInsuranceAccountMutation.Field()
    update_insurance_account = UpdateInsuranceAccountMutation.Field()
    delete_insurance_account = DeleteInsuranceAccountMutation.Field()

    create_appointment = CreateAppointmentMutation.Field()
    update_appointment = UpdateAppointmentMutation.Field()
    delete_appointment = DeleteAppointmentMutation.Field()

    create_consultation = CreateConsultationMutation.Field()
    update_consultation = UpdateConsultationMutation.Field()
    delete_consultation = DeleteConsultationMutation.Field()

    create_bill = CreateBillMutation.Field()
    update_bill = UpdateBillMutation.Field()
    delete_bill = DeleteBillMutation.Field()

    create_prescription = CreatePrescriptionMutation.Field()
    update_prescription = UpdatePrescriptionMutation.Field()
    delete_prescription = DeletePrescriptionMutation.Field()

    create_address = CreateAddressMutation.Field()
    update_address = UpdateAddressMutation.Field()
    delete_address = DeleteAddressMutation.Field()

    create_common_info = CreateCommonInfoMutation.Field()
    update_common_info = UpdateCommonInfoMutation.Field()
    delete_common_info = DeleteCommonInfoMutation.Field()

    create_insurance_agency = CreateInsuranceAgencyMutation.Field()
    update_insurance_agency = UpdateInsuranceAgencyMutation.Field()
    delete_insurance_agency = DeleteInsuranceAgencyMutation.Field()

# Define el esquema principal de GraphQL que incluye la consulta y las mutaciones
schema = graphene.Schema(query=Query, mutation=Mutation)
