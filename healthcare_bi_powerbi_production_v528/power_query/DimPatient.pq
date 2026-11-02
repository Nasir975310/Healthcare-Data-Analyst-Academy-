let
    FolderPath = "C:\HDA\healthcare_bi_powerbi_production_v528\data",
    Source = Csv.Document(File.Contents(FolderPath & "\patients.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"PatientID", type text}, {"Gender", type text}, {"BirthDate", type date}, {"Residence", type text}, {"Region", type text}})
in
    Typed
