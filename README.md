# Uncertainties of the Archives
We explored uncertainties and ambiguities in geographical data provided by the Ethnological Museum in Berlin. Our data consists of semi-structured information about people and corporations connected to the museum until 1950 ([Culture Translocated: Entities in the Ethnological Museum – Stabi Lab](https://lab.sbb.berlin/culture-translocated/)).

After preprocessing using a simple Python script, we examined the data more closely and noticed that some places appear with many different spellings (e.g. Frankfurt) or include markers of uncertainty (e.g. question marks). Digging deeper revealed more complex challenges that we could not address automatically:
- **Same name – different place**: A single name refers to different geographical entities, e.g. *Bali*, which represents an island in Indonesia as well as a town and neighbourhood in modern Cameroon.
- **Same place – different name**: Different place names may refer to the same geographical entity due to varying spellings across languages (e.g. *Wrocław* and *Breslau*) or changes in name/attribution over time (*Lahore (Pakistan)* / *Lahore (Indien)* / *Lahore (Britisch-Indien)*)
- **Different levels of precision**: Some names refer to cities, while others refer to broader regions or former colonies

Using our expertise, we combined place names referring to the same location into a single entry within the available timeframe. To obtain corresponding geographical information in a computer-readable format, we used the [GeoNames API](https://www.geonames.org/export/web-services.html) and visualized all the data point we could find as a heatmap using QGIS.

We view the process of data preprocessing as a method to explore (cultural) data and gain initial insight into its structure and challenges.
To present our findings about ambiguities in geographical data with colonial contexts, we created a little fun quiz named "GuineaPick" to allow the audience to experience the difficulties of mapping historical geographical data.

<img width="2500" height="1700" alt="guineapick_cover" src="https://github.com/user-attachments/assets/256cc0c5-f924-434e-9f0a-0b3c57e8effe" />
