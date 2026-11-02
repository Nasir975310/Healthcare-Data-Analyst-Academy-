let
    FolderPath = "C:\HDA\healthcare_bi_powerbi_production_v528\data",
    Source = Csv.Document(File.Contents(FolderPath & "\medications.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"MedicationID", type text}, {"EncounterID", type text}, {"Medication", type text}, {"DrugClass", type text}, {"IsActive", Int64.Type}})
in
    Typed
