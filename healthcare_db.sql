 1.
CREATE TABLE Patients (
    PatientID INT PRIMARY KEY,
    FullName VARCHAR(100),
    Age INT,
    City VARCHAR(50),
    ChronicCondition BOOLEAN -- האם יש מחלה כרונית (משפיע על הגעה)
);

 2. 
CREATE TABLE Doctors (
    DoctorID INT PRIMARY KEY,
    DoctorName VARCHAR(100),
    Department VARCHAR(50) -- קרדיולוגיה, עיניים, משפחה וכו'
);

 3. 
CREATE TABLE Appointments (
    AppointmentID INT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    AppointmentDate DATE,
    WaitTimeMinutes INT, -- כמה זמן המטופל חיכה בפועל
    Status VARCHAR(20), -- 'Show', 'No-Show', 'Cancelled'
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
);
