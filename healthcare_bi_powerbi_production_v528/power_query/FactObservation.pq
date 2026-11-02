let
    FolderPath = "C:\HDA\healthcare_bi_powerbi_production_v528\data",
    Source = Csv.Document(File.Contents(FolderPath & "\observations.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"ObservationID", type text}, {"EncounterID", type text}, {"Measure", type text}, {"Value", type number}, {"Unit", type text}})
in
    Typed
