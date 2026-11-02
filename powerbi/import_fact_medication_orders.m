// Power Query M — import one CSV as a typed query.
// Repeat for each supplied CSV and change the file name and type map.
// Example for FactMedicationOrders. Update the path for your computer.
let
    Source = Csv.Document(
        File.Contents("C:\HDA_Academy\assignments\data\pbi_fact_medication_orders.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TypedColumns = Table.TransformColumnTypes(PromotedHeaders,{
        {"order_id", type text}, {"encounter_key", type text},
        {"order_date", type date}, {"drug_key", type text},
        {"therapeutic_class", type text}, {"route", type text},
        {"order_status", type text}, {"quantity", Int64.Type},
        {"unit_cost_inr", type number}, {"line_total_inr", type number},
        {"prescriber_id", type text}, {"pharmacy_location", type text}
    }),
    CleanText = Table.TransformColumns(TypedColumns,{
        {"encounter_key", each Text.Trim(_), type text},
        {"drug_key", each Text.Trim(_), type text},
        {"order_status", each Text.Upper(Text.Trim(_)), type text}
    })
in
    CleanText
