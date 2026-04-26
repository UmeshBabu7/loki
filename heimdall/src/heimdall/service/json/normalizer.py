import json

from heimdall.service.json.config import JSONNormalizerConfig

TABLE_FIELDS = ["RuleID", "File", "StartLine", "Description"]


class JSONNormalizerService:
    def __init__(self, config: JSONNormalizerConfig):
        self.config = config

    def _validate_and_parse(self) -> list:
        validated = []
        for entry in self.config.data:
            parsed = self.config.schema.model_validate(entry)
            validated.append(parsed)
        return validated

    def _filter_fields(self, records: list) -> list:
        filtered = []
        for record in records:
            row = {
                field: getattr(record, field)
                for field in TABLE_FIELDS
                if hasattr(record, field)
            }
            if "Date" in row and hasattr(row["Date"], "isoformat"):
                row["Date"] = row["Date"].isoformat()
            filtered.append(row)
        return filtered

    def normalize_json(self) -> None:
        records = self._validate_and_parse()
        filtered = self._filter_fields(records)

        output_path = self.config.output_file_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(filtered, f, indent=2)

        print(f"Filtered JSON written to: {output_path}")
