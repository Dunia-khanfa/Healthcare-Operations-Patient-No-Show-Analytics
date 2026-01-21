 1.
CREATE TABLE Patients (
    PatientID INT PRIMARY KEY,
    FullName VARCHAR(100),
    Age INT,
    City VARCHAR(50),
    ChronicCondition BOOLEAN 
);

 2. 
CREATE TABLE Doctors (
    DoctorID INT PRIMARY KEY,
    DoctorName VARCHAR(100),
    Department VARCHAR(50) 
);

 3. 
CREATE TABLE Appointments (
    AppointmentID INT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    AppointmentDate DATE,
    WaitTimeMinutes INT,
    Status VARCHAR(20), -- 'Show', 'No-Show', 'Cancelled'
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
);
