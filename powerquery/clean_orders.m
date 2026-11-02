// Healthcare Data Analyst Academy v2.2.0
// Reference Power Query M pattern. Adapt file paths and query names in Excel.
// Not executed in Power Query Desktop during package QA.
// Keep source queries Raw_Orders and Raw_Encounters unchanged.

let
    Source = Csv.Document(
        File.Contents("C:\HDA_Academy\assignments\data\excel_raw_medication_orders.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers,{
        {"order_id", type text}, {"encounter_id", type text},
        {"order_date", type date}, {"drug_name", type text},
        {"therapeutic_class", type text}, {"route", type text},
        {"order_status", type text}, {"quantity", Int64.Type},
        {"unit_cost_inr", type number}, {"prescriber_id", type text},
        {"pharmacy_location", type text}, {"line_total_inr", type number}
    }),
    CleanText = Table.TransformColumns(Types,{
        {"drug_name", each if _ = null then null else Text.Trim(Text.Clean(_)), type text},
        {"therapeutic_class", each if _ = null then null else Text.Trim(Text.Clean(_)), type text},
        {"order_status", each if _ = null then null else Text.Upper(Text.Trim(Text.Clean(_))), type text},
        {"encounter_id", each if _ = null then null else Text.Trim(_), type text}
    }),
    AddMissingClassFlag = Table.AddColumn(CleanText, "missing_class_flag",
        each [therapeutic_class] = null or [therapeutic_class] = "", type logical),
    AddMissingCostFlag = Table.AddColumn(AddMissingClassFlag, "missing_cost_flag",
        each [unit_cost_inr] = null, type logical),
    Encounters = Excel.CurrentWorkbook(){[Name="tblEncounters"]}[Content],
    EncounterKeys = Table.Distinct(Table.SelectColumns(Encounters,{"encounter_id"})),
    JoinEncounter = Table.NestedJoin(AddMissingCostFlag, {"encounter_id"},
        EncounterKeys, {"encounter_id"}, "EncounterMatch", JoinKind.LeftOuter),
    AddOrphanFlag = Table.AddColumn(JoinEncounter, "orphan_encounter_flag",
        each Table.IsEmpty([EncounterMatch]), type logical),
    RemoveJoinHelper = Table.RemoveColumns(AddOrphanFlag,{"EncounterMatch"})
in
    RemoveJoinHelper

// Duplicate review guidance:
// Do not remove duplicates solely by order_id. The supplied source IDs are unique.
// Build a separate candidate review using a business key such as
// encounter_id + order_date + drug_name + route + quantity, then inspect candidates.
// Retain a reviewed audit column and preserve the unmodified source query.
