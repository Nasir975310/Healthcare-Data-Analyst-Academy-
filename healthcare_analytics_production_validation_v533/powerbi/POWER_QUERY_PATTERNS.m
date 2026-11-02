// Pattern only: replace parameter and field names after inspecting actual source schema.
let
    Source = Csv.Document(
        File.Contents(pEncounterCsv),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"encounter_id", type text},
        {"patient_id", type text},
        {"encounter_date", type date},
        {"encounter_type", type text}
    }),
    Normalized = Table.TransformColumns(Typed, {
        {"encounter_id", each Text.Trim(_), type text},
        {"patient_id", each Text.Trim(_), type text},
        {"encounter_type", each Text.Upper(Text.Trim(_)), type text}
    }),
    WithSourceRow = Table.AddIndexColumn(Normalized, "source_row_number", 1, 1, Int64.Type)
in
    WithSourceRow
