let
    Source = Csv.Document(
        File.Contents("C:\\HealthcareAnalytics\\data\\encounters.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers,{
        {"encounter_id", type text}, {"patient_id", type text},
        {"department_id", type text}, {"department_name", type text},
        {"encounter_date", type date}, {"encounter_type", type text},
        {"discharge_status", type text}, {"los_days", Int64.Type},
        {"charge_inr", Currency.Type}
    }),
    Trimmed = Table.TransformColumns(Types,{
        {"encounter_id", Text.Trim, type text},
        {"patient_id", Text.Trim, type text},
        {"department_id", Text.Trim, type text}
    }),
    ValidRows = Table.SelectRows(Trimmed, each
        [encounter_id] <> null and [encounter_id] <> "" and
        [patient_id] <> null and [encounter_date] <> null and
        [los_days] >= 0 and [charge_inr] >= 0
    ),
    AddMonth = Table.AddColumn(ValidRows, "YearMonth",
        each Date.ToText([encounter_date], "yyyy-MM"), type text),
    AddEncounterCount = Table.AddColumn(AddMonth, "EncounterCount",
        each 1, Int64.Type)
in
    AddEncounterCount
