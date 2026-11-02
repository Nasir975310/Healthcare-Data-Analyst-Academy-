let
    FolderPath = "C:\HDA\healthcare_bi_powerbi_production_v528\data",
    Source = Csv.Document(File.Contents(FolderPath & "\encounters.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"EncounterID", type text}, {"PatientID", type text}, {"EncounterDate", type date}, {"EncounterType", type text}, {"Status", type text}})
in
    Typed
