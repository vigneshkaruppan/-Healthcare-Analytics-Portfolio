
USE ClinicalLIMS_Portfolio;
GO
CREATE TABLE Departments (
    DepartmentID   INT IDENTITY(1,1) PRIMARY KEY,
    DeptName       VARCHAR(100) NOT NULL,
    DeptCode       VARCHAR(10)  NOT NULL UNIQUE,
    HeadOfDept     VARCHAR(100),
    ContactNo      VARCHAR(15),
    IsActive       BIT DEFAULT 1
);
GO

CREATE TABLE Patients (
    PatientID      INT IDENTITY(1001,1) PRIMARY KEY,
    PatientName    VARCHAR(100) NOT NULL,
    Age            INT          NOT NULL,
    Gender         VARCHAR(10)  NOT NULL CHECK (Gender IN ('Male','Female','Other')),
    BloodGroup     VARCHAR(5),
    ContactNo      VARCHAR(15),
    City           VARCHAR(50),
    RegisteredDate DATE         DEFAULT GETDATE()
);
GO

CREATE TABLE Tests (
    TestID         INT IDENTITY(1,1) PRIMARY KEY,
    TestName       VARCHAR(100) NOT NULL,
    TestCode       VARCHAR(20)  NOT NULL UNIQUE,
    DepartmentID   INT          REFERENCES Departments(DepartmentID),
    NormalRangeLow FLOAT,
    NormalRangeHigh FLOAT,
    Unit           VARCHAR(20),
    TATHoursTarget INT DEFAULT 6
);
GO

CREATE TABLE Samples (
    SampleID         INT IDENTITY(10001,1) PRIMARY KEY,
    PatientID        INT          REFERENCES Patients(PatientID),
    TestID           INT          REFERENCES Tests(TestID),
    DepartmentID     INT          REFERENCES Departments(DepartmentID),
    CollectionDate   DATETIME     NOT NULL DEFAULT GETDATE(),
    ReportDate       DATETIME,
    TAT_Hours        AS DATEDIFF(HOUR, CollectionDate, ReportDate),  -- Computed column
    Status           VARCHAR(20)  DEFAULT 'Pending'
                                  CHECK (Status IN ('Pending','Processing',
                                                    'Completed','Delayed','Rejected')),
    TechnicianName   VARCHAR(100),
    Priority         VARCHAR(10)  DEFAULT 'Normal'
                                  CHECK (Priority IN ('Normal','Urgent','STAT')),
    SampleType       VARCHAR(50),
    Remarks          VARCHAR(255)
);
GO


CREATE TABLE Results (
    ResultID       INT IDENTITY(1,1) PRIMARY KEY,
    SampleID       INT          REFERENCES Samples(SampleID),
    ResultValue    FLOAT,
    ResultText     VARCHAR(255),
    ResultStatus   VARCHAR(20)  CHECK (ResultStatus IN ('Normal','Abnormal','Critical')),
    VerifiedBy     VARCHAR(100),
    VerifiedDate   DATETIME     DEFAULT GETDATE(),
    QC_Status      VARCHAR(10)  DEFAULT 'Pass'
                                CHECK (QC_Status IN ('Pass','Fail','Repeat'))
);
GO

CREATE TABLE QC_Control (
    QC_ID          INT IDENTITY(1,1) PRIMARY KEY,
    TestID         INT          REFERENCES Tests(TestID),
    ControlDate    DATE         DEFAULT GETDATE(),
    ControlLevel   VARCHAR(20),  -- Level 1 / Level 2 / Level 3
    MeasuredValue  FLOAT        NOT NULL,
    TargetMean     FLOAT,
    SD             FLOAT,
    WestgardRule   VARCHAR(20),  -- 1:2s / 1:3s / 2:2s / R:4s
    QC_Result      VARCHAR(10)  DEFAULT 'Pass'
);
GO


CREATE NONCLUSTERED INDEX IX_Samples_PatientID
    ON Samples(PatientID);
 
CREATE NONCLUSTERED INDEX IX_Samples_Status
    ON Samples(Status);
 
CREATE NONCLUSTERED INDEX IX_Samples_CollectionDate
    ON Samples(CollectionDate);
 
CREATE NONCLUSTERED INDEX IX_Samples_DepartmentID
    ON Samples(DepartmentID);
 
CREATE NONCLUSTERED INDEX IX_Results_SampleID
    ON Results(SampleID);
 
CREATE NONCLUSTERED INDEX IX_Results_ResultStatus
    ON Results(ResultStatus);
 
INSERT INTO Departments (DeptName, DeptCode, HeadOfDept, ContactNo)
VALUES
    ('Haematology',       'HAEM', 'Dr. Rajesh Kumar',   '9876543210'),
    ('Clinical Biochemistry', 'BIOC', 'Dr. Priya Sharma', '9876543211'),
    ('Microbiology',      'MICR', 'Dr. Suresh Nair',    '9876543212'),
    ('Blood Banking',     'BBKG', 'Dr. Anitha Devi',    '9876543213'),
    ('Histopathology',    'HIST', 'Dr. Vijay Mohan',    '9876543214');
GO

INSERT INTO Patients (PatientName, Age, Gender, BloodGroup, ContactNo, City)
VALUES
    ('Ravi Kumar',      35, 'Male',   'O+', '9876500001', 'Coimbatore'),
    ('Priya Shankar',   28, 'Female', 'A+', '9876500002', 'Chennai'),
    ('Suresh Babu',     45, 'Male',   'B+', '9876500003', 'Madurai'),
    ('Anitha Devi',     32, 'Female', 'AB+','9876500004', 'Trichy'),
    ('Karthik Raja',    52, 'Male',   'O-', '9876500005', 'Coimbatore'),
    ('Meena Ravi',      29, 'Female', 'A-', '9876500006', 'Salem'),
    ('Arjun Pandian',   41, 'Male',   'B-', '9876500007', 'Erode'),
    ('Divya Raj',       38, 'Female', 'O+', '9876500008', 'Coimbatore'),
    ('Mani Kandan',     60, 'Male',   'A+', '9876500009', 'Karur'),
    ('Kavitha Nair',    25, 'Female', 'B+', '9876500010', 'Namakkal');
GO

INSERT INTO Tests (TestName, TestCode, DepartmentID, NormalRangeLow, NormalRangeHigh, Unit, TATHoursTarget)
VALUES
    ('Complete Blood Count',   'CBC',   1, 4.5,  11.0, 'x10^3/uL', 4),
    ('Haemoglobin',            'HB',    1, 12.0, 17.0, 'g/dL',     4),
    ('Platelet Count',         'PLT',   1, 150,  400,  'x10^3/uL', 4),
    ('Glucose Fasting',        'FBS',   2, 70.0, 100.0,'mg/dL',    3),
    ('Creatinine',             'CREAT', 2, 0.6,  1.2,  'mg/dL',    3),
    ('Urea',                   'UREA',  2, 15.0, 45.0, 'mg/dL',    3),
    ('SGOT',                   'SGOT',  2, 10.0, 40.0, 'U/L',      4),
    ('SGPT',                   'SGPT',  2, 7.0,  56.0, 'U/L',      4),
    ('Gram Stain',             'GRAM',  3, NULL,  NULL, 'Report',   6),
    ('Culture & Sensitivity',  'CULT',  3, NULL,  NULL, 'Report',   48),
    ('ABO Blood Grouping',     'ABO',   4, NULL,  NULL, 'Group',    2),
    ('Cross Match',            'XMATCH',4, NULL,  NULL, 'Result',   4);
GO
 
 INSERT INTO Samples (PatientID, TestID, DepartmentID, CollectionDate, ReportDate, 
                     Status, TechnicianName, Priority, SampleType)
VALUES
    (1001, 1, 1, '2026-06-01 08:00', '2026-06-01 11:30', 'Completed', 'Tech A', 'Normal',  'Whole Blood'),
    (1001, 4, 2, '2026-06-01 08:00', '2026-06-01 10:00', 'Completed', 'Tech B', 'Urgent',  'Serum'),
    (1002, 2, 1, '2026-06-01 09:00', '2026-06-01 15:00', 'Delayed',   'Tech A', 'Normal',  'Whole Blood'),
    (1002, 5, 2, '2026-06-01 09:00', '2026-06-01 11:30', 'Completed', 'Tech C', 'Normal',  'Serum'),
    (1003, 3, 1, '2026-06-02 08:30', '2026-06-02 12:00', 'Delayed',   'Tech B', 'Normal',  'Whole Blood'),
    (1003, 6, 2, '2026-06-02 08:30', '2026-06-02 11:00', 'Completed', 'Tech D', 'Normal',  'Serum'),
    (1004, 7, 2, '2026-06-02 10:00', '2026-06-02 14:30', 'Delayed',   'Tech C', 'Normal',  'Serum'),
    (1004, 8, 2, '2026-06-02 10:00', '2026-06-02 14:00', 'Delayed',   'Tech C', 'Normal',  'Serum'),
    (1005, 9, 3, '2026-06-03 08:00', '2026-06-03 16:00', 'Completed', 'Tech E', 'Normal',  'Sputum'),
    (1005,10, 3, '2026-06-03 08:00', '2026-06-05 10:00', 'Completed', 'Tech E', 'Normal',  'Urine'),
    (1006,11, 4, '2026-06-03 09:00', '2026-06-03 10:30', 'Completed', 'Tech F', 'Urgent',  'Whole Blood'),
    (1006,12, 4, '2026-06-03 09:00', '2026-06-03 13:00', 'Completed', 'Tech F', 'Urgent',  'Whole Blood'),
    (1007, 1, 1, '2026-06-04 08:00', '2026-06-04 18:00', 'Delayed',   'Tech A', 'Normal',  'Whole Blood'),
    (1007, 4, 2, '2026-06-04 08:00', '2026-06-04 10:30', 'Completed', 'Tech B', 'STAT',    'Serum'),
    (1008, 2, 1, '2026-06-04 09:30', '2026-06-04 13:00', 'Completed', 'Tech A', 'Normal',  'Whole Blood'),
    (1008, 5, 2, '2026-06-04 09:30', '2026-06-04 12:30', 'Completed', 'Tech D', 'Normal',  'Serum'),
    (1009, 3, 1, '2026-06-05 08:00', '2026-06-05 20:00', 'Delayed',   'Tech B', 'Normal',  'Whole Blood'),
    (1009, 6, 2, '2026-06-05 08:00', '2026-06-05 11:00', 'Completed', 'Tech C', 'Normal',  'Serum'),
    (1010, 7, 2, '2026-06-05 10:00', '2026-06-05 14:00', 'Completed', 'Tech D', 'Normal',  'Serum'),
    (1010, 1, 1, '2026-06-05 10:00', '2026-06-05 14:30', 'Completed', 'Tech A', 'Normal',  'Whole Blood');
GO

INSERT INTO Results (SampleID, ResultValue, ResultText, ResultStatus, VerifiedBy, QC_Status)
VALUES
    (10001, 8.5,  NULL,      'Normal',   'Dr. Rajesh',  'Pass'),
    (10002, 95.0, NULL,      'Normal',   'Dr. Priya',   'Pass'),
    (10003, 9.8,  NULL,      'Abnormal', 'Dr. Rajesh',  'Pass'),
    (10004, 1.8,  NULL,      'Abnormal', 'Dr. Priya',   'Pass'),
    (10005, 120,  NULL,      'Normal',   'Dr. Rajesh',  'Pass'),
    (10006, 55.0, NULL,      'Abnormal', 'Dr. Priya',   'Pass'),
    (10007, 65.0, NULL,      'Abnormal', 'Dr. Priya',   'Fail'),
    (10008, 85.0, NULL,      'Abnormal', 'Dr. Priya',   'Fail'),
    (10009, NULL, 'Gram +ve Cocci seen', 'Abnormal', 'Dr. Suresh', 'Pass'),
    (10010, NULL, 'E.coli sensitive to Amoxicillin', 'Abnormal', 'Dr. Suresh', 'Pass'),
    (10011, NULL, 'B Positive', 'Normal',  'Dr. Anitha',  'Pass'),
    (10012, NULL, 'Compatible', 'Normal',  'Dr. Anitha',  'Pass'),
    (10013, 6.2,  NULL,      'Normal',   'Dr. Rajesh',  'Pass'),
    (10014, 88.0, NULL,      'Normal',   'Dr. Priya',   'Pass'),
    (10015, 11.5, NULL,      'Normal',   'Dr. Rajesh',  'Pass'),
    (10016, 1.1,  NULL,      'Normal',   'Dr. Priya',   'Pass'),
    (10017, 85,   NULL,      'Normal',   'Dr. Rajesh',  'Pass'),
    (10018, 38.0, NULL,      'Normal',   'Dr. Priya',   'Pass'),
    (10019, 42.0, NULL,      'Normal',   'Dr. Priya',   'Pass'),
    (10020, 9.1,  NULL,      'Normal',   'Dr. Rajesh',  'Pass');
GO


INSERT INTO QC_Control (TestID, ControlDate, ControlLevel, MeasuredValue, TargetMean, SD)
VALUES
    (1, '2026-06-01', 'Level 1', 8.5,  8.0, 0.5),
    (1, '2026-06-02', 'Level 1', 8.1,  8.0, 0.5),
    (1, '2026-06-03', 'Level 1', 9.2,  8.0, 0.5),
    (1, '2026-06-04', 'Level 1', 7.6,  8.0, 0.5),
    (1, '2026-06-05', 'Level 1', 8.9,  8.0, 0.5),
    (1, '2026-06-06', 'Level 1', 10.2, 8.0, 0.5),
    (1, '2026-06-07', 'Level 1', 7.2,  8.0, 0.5),
    (4, '2026-06-01', 'Level 1', 98.0, 100.0, 2.0),
    (4, '2026-06-02', 'Level 1', 101.5,100.0, 2.0),
    (4, '2026-06-03', 'Level 1', 97.5, 100.0, 2.0),
    (4, '2026-06-04', 'Level 1', 104.8,100.0, 2.0),
    (4, '2026-06-05', 'Level 1', 109.2,100.0, 2.0),
    (4, '2026-06-06', 'Level 1', 94.8, 100.0, 2.0),
    (4, '2026-06-07', 'Level 1', 98.5, 100.0, 2.0);
GO

SELECT
    d.DeptName                          AS Department,
    COUNT(s.SampleID)                   AS TotalSamples,
    AVG(CAST(s.TAT_Hours AS FLOAT))     AS AvgTAT_Hours,
    MIN(s.TAT_Hours)                    AS MinTAT,
    MAX(s.TAT_Hours)                    AS MaxTAT,
    SUM(CASE WHEN s.Status = 'Delayed'
             THEN 1 ELSE 0 END)         AS DelayedCount,
    CAST(SUM(CASE WHEN s.Status = 'Delayed'
             THEN 1.0 ELSE 0 END)
         / COUNT(s.SampleID) * 100
         AS DECIMAL(5,2))               AS DelayRate_Pct
FROM Samples s
JOIN Departments d ON s.DepartmentID = d.DepartmentID
WHERE s.ReportDate IS NOT NULL
GROUP BY d.DeptName
ORDER BY DelayRate_Pct DESC;
GO
 
 SELECT
    p.PatientID,
    p.PatientName,
    p.Age,
    p.Gender,
    t.TestName,
    d.DeptName          AS Department,
    s.CollectionDate,
    s.ReportDate,
    s.TAT_Hours,
    s.Status,
    r.ResultValue,
    r.ResultStatus,
    r.QC_Status
FROM Samples s
JOIN Patients    p ON s.PatientID    = p.PatientID
JOIN Tests       t ON s.TestID       = t.TestID
JOIN Departments d ON s.DepartmentID = d.DepartmentID
LEFT JOIN Results r ON s.SampleID   = r.SampleID
ORDER BY p.PatientID, s.CollectionDate;
GO

SELECT
    s.SampleID,
    p.PatientName,
    t.TestName,
    d.DeptName,
    t.TATHoursTarget    AS TargetTAT,
    s.TAT_Hours         AS ActualTAT,
    s.TAT_Hours - t.TATHoursTarget AS ExceededBy_Hours,
    s.TechnicianName,
    s.Priority
FROM Samples s
JOIN Patients    p ON s.PatientID    = p.PatientID
JOIN Tests       t ON s.TestID       = t.TestID
JOIN Departments d ON s.DepartmentID = d.DepartmentID
WHERE s.TAT_Hours > t.TATHoursTarget
ORDER BY ExceededBy_Hours DESC;
GO


SELECT
    s.TechnicianName,
    COUNT(s.SampleID)                  AS TotalSamples,
    AVG(CAST(s.TAT_Hours AS FLOAT))    AS AvgTAT,
    SUM(CASE WHEN s.Status = 'Delayed'
             THEN 1 ELSE 0 END)        AS DelayedSamples,
    SUM(CASE WHEN s.Status = 'Completed'
             THEN 1 ELSE 0 END)        AS CompletedOnTime,
    CAST(SUM(CASE WHEN s.Status = 'Completed'
             THEN 1.0 ELSE 0 END)
         / COUNT(*) * 100
         AS DECIMAL(5,2))              AS OnTimeRate_Pct
FROM Samples s
WHERE s.ReportDate IS NOT NULL
GROUP BY s.TechnicianName
ORDER BY OnTimeRate_Pct DESC;
GO

SELECT
    s.SampleID,
    p.PatientName,
    d.DeptName,
    t.TestName,
    s.TAT_Hours,
    RANK() OVER (PARTITION BY d.DeptName
                 ORDER BY s.TAT_Hours DESC)     AS DelayRank_InDept,
    AVG(CAST(s.TAT_Hours AS FLOAT))
        OVER (PARTITION BY d.DeptName)          AS DeptAvgTAT,
    s.TAT_Hours - AVG(CAST(s.TAT_Hours AS FLOAT))
        OVER (PARTITION BY d.DeptName)          AS DeviationFromAvg,
    LAG(s.TAT_Hours) OVER (PARTITION BY d.DeptName
                           ORDER BY s.CollectionDate) AS PrevSampleTAT,
    SUM(s.TAT_Hours) OVER (PARTITION BY d.DeptName
                           ORDER BY s.CollectionDate
                           ROWS BETWEEN 2 PRECEDING
                           AND CURRENT ROW)     AS Rolling3SampleTAT
FROM Samples s
JOIN Patients    p ON s.PatientID    = p.PatientID
JOIN Tests       t ON s.TestID       = t.TestID
JOIN Departments d ON s.DepartmentID = d.DepartmentID
WHERE s.ReportDate IS NOT NULL
ORDER BY d.DeptName, s.TAT_Hours DESC;
GO
 
 SELECT
    qc.QC_ID,
    t.TestName,
    qc.ControlDate,
    qc.ControlLevel,
    qc.MeasuredValue,
    qc.TargetMean,
    qc.SD,
    CAST((qc.MeasuredValue - qc.TargetMean)
         / qc.SD AS DECIMAL(4,2))         AS Z_Score,
    CASE
        WHEN ABS(qc.MeasuredValue - qc.TargetMean)
             > 3 * qc.SD THEN '1:3s VIOLATION - REJECT RUN'
        WHEN ABS(qc.MeasuredValue - qc.TargetMean)
             > 2 * qc.SD THEN '1:2s WARNING'
        ELSE 'Within Control'
    END                                    AS WestgardStatus
FROM QC_Control qc
JOIN Tests t ON qc.TestID = t.TestID
ORDER BY qc.TestID, qc.ControlDate;
GO

SELECT
    p.PatientName,
    p.Age,
    p.Gender,
    t.TestName,
    r.ResultValue,
    t.NormalRangeLow    AS RefLow,
    t.NormalRangeHigh   AS RefHigh,
    t.Unit,
    r.ResultStatus,
    CASE
        WHEN r.ResultValue < t.NormalRangeLow  THEN 'LOW ↓'
        WHEN r.ResultValue > t.NormalRangeHigh THEN 'HIGH ↑'
        ELSE 'Normal'
    END                 AS FlagStatus,
    r.VerifiedBy,
    r.QC_Status
FROM Results r
JOIN Samples  s ON r.SampleID   = s.SampleID
JOIN Patients p ON s.PatientID  = p.PatientID
JOIN Tests    t ON s.TestID     = t.TestID
WHERE r.ResultStatus IN ('Abnormal','Critical')
ORDER BY r.ResultStatus DESC, p.PatientName;
GO

SELECT
    CAST(CollectionDate AS DATE)    AS WorkDate,
    COUNT(SampleID)                 AS TotalReceived,
    SUM(CASE WHEN Status = 'Completed' THEN 1 ELSE 0 END) AS Completed,
    SUM(CASE WHEN Status = 'Delayed'   THEN 1 ELSE 0 END) AS Delayed,
    SUM(CASE WHEN Status = 'Pending'   THEN 1 ELSE 0 END) AS Pending,
    SUM(CASE WHEN Priority = 'STAT'    THEN 1 ELSE 0 END) AS STAT_Samples,
    SUM(CASE WHEN Priority = 'Urgent'  THEN 1 ELSE 0 END) AS Urgent_Samples
FROM Samples
GROUP BY CAST(CollectionDate AS DATE)
ORDER BY WorkDate;
GO

CREATE OR ALTER PROCEDURE sp_GetSamplesByDepartment
    @DeptCode VARCHAR(10)
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        s.SampleID,
        p.PatientName,
        t.TestName,
        s.CollectionDate,
        s.ReportDate,
        s.TAT_Hours,
        t.TATHoursTarget,
        s.Status,
        s.TechnicianName,
        s.Priority
    FROM Samples s
    JOIN Patients    p ON s.PatientID    = p.PatientID
    JOIN Tests       t ON s.TestID       = t.TestID
    JOIN Departments d ON s.DepartmentID = d.DepartmentID
    WHERE d.DeptCode = @DeptCode
    ORDER BY s.CollectionDate DESC;
END;
GO

CREATE OR ALTER PROCEDURE sp_GetDelayedSamples
    @DeptCode   VARCHAR(10) = NULL,
    @FromDate   DATE        = NULL,
    @ToDate     DATE        = NULL
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        s.SampleID,
        p.PatientName,
        p.ContactNo,
        t.TestName,
        d.DeptName,
        s.CollectionDate,
        s.ReportDate,
        s.TAT_Hours                         AS ActualTAT,
        t.TATHoursTarget                    AS TargetTAT,
        s.TAT_Hours - t.TATHoursTarget      AS BreachHours,
        s.TechnicianName,
        s.Priority
    FROM Samples s
    JOIN Patients    p ON s.PatientID    = p.PatientID
    JOIN Tests       t ON s.TestID       = t.TestID
    JOIN Departments d ON s.DepartmentID = d.DepartmentID
    WHERE s.Status = 'Delayed'
      AND (@DeptCode IS NULL OR d.DeptCode = @DeptCode)
      AND (@FromDate IS NULL OR CAST(s.CollectionDate AS DATE) >= @FromDate)
      AND (@ToDate   IS NULL OR CAST(s.CollectionDate AS DATE) <= @ToDate)
    ORDER BY BreachHours DESC;
END;
GO

CREATE OR ALTER PROCEDURE sp_GetAvgTAT
    @DeptCode   VARCHAR(10),
    @AvgTAT     FLOAT OUTPUT,
    @TotalCount INT   OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        @AvgTAT     = AVG(CAST(s.TAT_Hours AS FLOAT)),
        @TotalCount = COUNT(s.SampleID)
    FROM Samples s
    JOIN Departments d ON s.DepartmentID = d.DepartmentID
    WHERE d.DeptCode = @DeptCode
      AND s.ReportDate IS NOT NULL;
END;
GO
 

 CREATE OR ALTER PROCEDURE sp_AddSample
    @PatientID      INT,
    @TestID         INT,
    @DepartmentID   INT,
    @TechnicianName VARCHAR(100),
    @Priority       VARCHAR(10) = 'Normal',
    @SampleType     VARCHAR(50) = NULL,
    @NewSampleID    INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        -- Validate patient exists
        IF NOT EXISTS (SELECT 1 FROM Patients WHERE PatientID = @PatientID)
        BEGIN
            RAISERROR('Patient ID %d does not exist', 16, 1, @PatientID);
            RETURN;
        END
         -- Validate test exists
        IF NOT EXISTS (SELECT 1 FROM Tests WHERE TestID = @TestID)
        BEGIN
            RAISERROR('Test ID %d does not exist', 16, 1, @TestID);
            RETURN;
        END

         INSERT INTO Samples
            (PatientID, TestID, DepartmentID, CollectionDate,
             Status, TechnicianName, Priority, SampleType)
        VALUES
            (@PatientID, @TestID, @DepartmentID, GETDATE(),
             'Pending', @TechnicianName, @Priority, @SampleType);
 
        SET @NewSampleID = SCOPE_IDENTITY();
        PRINT 'Sample added successfully. SampleID = ' + CAST(@NewSampleID AS VARCHAR);
    END TRY
    BEGIN CATCH
        PRINT 'Error: ' + ERROR_MESSAGE();
    END CATCH
END;
GO
       
       CREATE OR ALTER PROCEDURE sp_UpdateTAT
    @SampleID   INT,
    @ReportDate DATETIME = NULL
AS
BEGIN
    SET NOCOUNT ON;
 
    IF @ReportDate IS NULL
        SET @ReportDate = GETDATE();
 
    UPDATE Samples
    SET ReportDate = @ReportDate
    WHERE SampleID = @SampleID;
 
    -- Auto-update status based on TAT
    UPDATE s
    SET s.Status = CASE
        WHEN s.TAT_Hours > t.TATHoursTarget THEN 'Delayed'
        ELSE 'Completed'
    END
    FROM Samples s
    JOIN Tests t ON s.TestID = t.TestID
    WHERE s.SampleID = @SampleID;
 
    PRINT 'TAT updated for SampleID: ' + CAST(@SampleID AS VARCHAR);
END;
GO
 
      CREATE OR ALTER PROCEDURE sp_GetPatientReport
    @PatientID INT
AS
BEGIN
    SET NOCOUNT ON;
 
    -- Patient details
    SELECT
        PatientID, PatientName, Age, Gender,
        BloodGroup, City, RegisteredDate
    FROM Patients
    WHERE PatientID = @PatientID;
 
    -- All test results
    SELECT
        t.TestName,
        d.DeptName,
        s.CollectionDate,
        s.TAT_Hours,
        s.Status,
        r.ResultValue,
        t.NormalRangeLow,
        t.NormalRangeHigh,
        t.Unit,
        r.ResultStatus,
        r.VerifiedBy
    FROM Samples s
    JOIN Tests    t ON s.TestID    = t.TestID
    JOIN Departments d ON s.DepartmentID = d.DepartmentID
    LEFT JOIN Results r ON s.SampleID  = r.SampleID
    WHERE s.PatientID = @PatientID
    ORDER BY s.CollectionDate DESC;
END;
GO 


CREATE OR ALTER PROCEDURE sp_GetQCViolations
    @TestID     INT  = NULL,
    @FromDate   DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        t.TestName,
        qc.ControlDate,
        qc.ControlLevel,
        qc.MeasuredValue,
        qc.TargetMean,
        qc.SD,
        CAST((qc.MeasuredValue - qc.TargetMean) / qc.SD
             AS DECIMAL(4,2))           AS Z_Score,
        CASE
            WHEN ABS(qc.MeasuredValue - qc.TargetMean)
                 > 3 * qc.SD THEN '1:3s - REJECT'
            WHEN ABS(qc.MeasuredValue - qc.TargetMean)
                 > 2 * qc.SD THEN '1:2s - WARNING'
            ELSE 'In Control'
        END                             AS WestgardRule
    FROM QC_Control qc
    JOIN Tests t ON qc.TestID = t.TestID
    WHERE (@TestID   IS NULL OR qc.TestID     = @TestID)
      AND (@FromDate IS NULL OR qc.ControlDate >= @FromDate)
      AND ABS(qc.MeasuredValue - qc.TargetMean) > qc.SD
    ORDER BY qc.ControlDate DESC;
END;
GO
 

 CREATE OR ALTER PROCEDURE sp_FilterSamples
    @Status     VARCHAR(20)  = NULL,
    @DeptCode   VARCHAR(10)  = NULL,
    @Priority   VARCHAR(10)  = NULL,
    @FromDate   DATE         = NULL,
    @ToDate     DATE         = NULL
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        s.SampleID,
        p.PatientName,
        t.TestName,
        d.DeptName,
        s.CollectionDate,
        s.TAT_Hours,
        s.Status,
        s.Priority,
        s.TechnicianName
    FROM Samples s
    JOIN Patients    p ON s.PatientID    = p.PatientID
    JOIN Tests       t ON s.TestID       = t.TestID
    JOIN Departments d ON s.DepartmentID = d.DepartmentID
    WHERE (@Status   IS NULL OR s.Status         = @Status)
      AND (@DeptCode IS NULL OR d.DeptCode        = @DeptCode)
      AND (@Priority IS NULL OR s.Priority        = @Priority)
      AND (@FromDate IS NULL OR CAST(s.CollectionDate AS DATE) >= @FromDate)
      AND (@ToDate   IS NULL OR CAST(s.CollectionDate AS DATE) <= @ToDate)
    ORDER BY s.CollectionDate DESC;
END;
GO


CREATE OR ALTER VIEW vw_LIMS_Dashboard AS
SELECT
    s.SampleID,
    p.PatientName,
    p.Age,
    p.Gender,
    p.City,
    t.TestName,
    t.TestCode,
    d.DeptName          AS Department,
    d.DeptCode,
    s.CollectionDate,
    s.ReportDate,
    s.TAT_Hours,
    t.TATHoursTarget,
    s.TAT_Hours - t.TATHoursTarget AS TAT_Breach_Hours,
    s.Status,
    s.Priority,
    s.TechnicianName,
    r.ResultValue,
    r.ResultStatus,
    r.QC_Status,
    CASE
        WHEN s.TAT_Hours > t.TATHoursTarget THEN 'Breached'
        ELSE 'Within SLA'
    END                 AS SLA_Status,
    CAST(s.CollectionDate AS DATE) AS CollectionDay,
    DATEPART(HOUR, s.CollectionDate) AS CollectionHour,
    DATENAME(WEEKDAY, s.CollectionDate) AS DayOfWeek
FROM Samples s
JOIN Patients    p ON s.PatientID    = p.PatientID
JOIN Tests       t ON s.TestID       = t.TestID
JOIN Departments d ON s.DepartmentID = d.DepartmentID
LEFT JOIN Results r ON s.SampleID   = r.SampleID;
GO


CREATE OR ALTER VIEW vw_QC_LeveyJennings AS
SELECT
    t.TestName,
    qc.ControlDate,
    qc.ControlLevel,
    qc.MeasuredValue,
    qc.TargetMean                       AS Mean,
    qc.TargetMean + qc.SD               AS Plus1SD,
    qc.TargetMean + (2 * qc.SD)         AS Plus2SD,
    qc.TargetMean + (3 * qc.SD)         AS Plus3SD,
    qc.TargetMean - qc.SD               AS Minus1SD,
    qc.TargetMean - (2 * qc.SD)         AS Minus2SD,
    qc.TargetMean - (3 * qc.SD)         AS Minus3SD,
    CAST((qc.MeasuredValue - qc.TargetMean)
         / qc.SD AS DECIMAL(4,2))       AS Z_Score,
    CASE
        WHEN ABS(qc.MeasuredValue - qc.TargetMean)
             > 3 * qc.SD THEN '1:3s REJECT'
        WHEN ABS(qc.MeasuredValue - qc.TargetMean)
             > 2 * qc.SD THEN '1:2s WARNING'
        ELSE 'In Control'
    END                                 AS WestgardFlag
FROM QC_Control qc
JOIN Tests t ON qc.TestID = t.TestID;
GO


CREATE OR ALTER VIEW vw_Technician_KPI AS
SELECT
    TechnicianName,
    COUNT(SampleID)                         AS TotalSamples,
    AVG(CAST(TAT_Hours AS FLOAT))           AS AvgTAT,
    SUM(CASE WHEN Status='Completed'
             THEN 1 ELSE 0 END)             AS OnTime,
    SUM(CASE WHEN Status='Delayed'
             THEN 1 ELSE 0 END)             AS Delayed,
    CAST(SUM(CASE WHEN Status='Completed'
             THEN 1.0 ELSE 0 END)
         / COUNT(*) * 100
         AS DECIMAL(5,2))                   AS OnTimeRate_Pct
FROM Samples
WHERE ReportDate IS NOT NULL
GROUP BY TechnicianName;
GO

 
EXEC sp_GetSamplesByDepartment @DeptCode = 'HAEM';
EXEC sp_GetDelayedSamples;
EXEC sp_GetPatientReport @PatientID = 1001;
EXEC sp_FilterSamples @Status = 'Delayed', @Priority = 'Normal';
EXEC sp_GetQCViolations;
 
-- Test output parameter
DECLARE @Avg FLOAT, @Count INT;
EXEC sp_GetAvgTAT @DeptCode='BIOC', @AvgTAT=@Avg OUTPUT, @TotalCount=@Count OUTPUT;
SELECT @Avg AS BiochemistryAvgTAT, @Count AS TotalBiochemSamples;

SELECT TOP 20 * FROM vw_LIMS_Dashboard ORDER BY CollectionDate DESC;
SELECT * FROM vw_QC_LeveyJennings;
SELECT * FROM vw_Technician_KPI ORDER BY OnTimeRate_Pct DESC;


SELECT * FROM vw_LIMS_Dashboard;

SELECT * FROM vw_QC_LeveyJennings;

SELECT
    COUNT(*) AS TotalSamples,
    AVG(CAST(TAT_Hours AS FLOAT)) AS AvgTAT,
    SUM(CASE WHEN Status='Delayed' THEN 1 ELSE 0 END) AS TotalDelayed,
    CAST(SUM(CASE WHEN Status='Delayed' THEN 1.0 ELSE 0 END)
         / COUNT(*) * 100 AS DECIMAL(5,2)) AS DelayRate_Pct,
    SUM(CASE WHEN Status='Completed' THEN 1 ELSE 0 END) AS TotalCompleted
FROM vw_LIMS_Dashboard;

 