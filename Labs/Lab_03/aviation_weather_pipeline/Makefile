.PHONY: all fetch analyze clean
all: analyze
fetch:
	@echo "--- Fetching data ---"
	bash ./fetch_metars.sh
	@echo "--- Data fetching complete ---"
analyze: fetch
	@echo "--- Analyzing data ---"
	bash ./analyze_data.sh
	@echo "--- Analysis complete ---"
	@echo "--- Pipeline complete ---"
clean:
	@echo "--- Cleaning up ---"
	rm -rf weather_report.csv
	rm -rf raw_metars/
	@echo "--- Cleaning complete ---"
