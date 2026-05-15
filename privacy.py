from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


def scrub_data(text):
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()

    results = analyzer.analyze(
        text=text,
        entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "LOCATION"],
        language="en"
    )

    return anonymizer.anonymize(text, results).text
