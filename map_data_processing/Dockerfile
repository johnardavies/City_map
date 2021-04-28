# Miniconda base image
FROM continuumio/miniconda:latest
RUN apt-get update && apt-get install -y libgtk2.0-dev 

# Install python and useful spatial datascience libraries   
RUN /opt/conda/bin/conda update -n base -c defaults conda && \
    /opt/conda/bin/conda install python=3.7 && \
    /opt/conda/bin/conda install anaconda-client && \
    /opt/conda/bin/conda install jupyter -y && \
    /opt/conda/bin/conda install geopandas numpy pandas scikit-learn matplotlib altair shapely  

RUN pip install plotnine
RUN pip install keplergl
RUN pip install geopy
RUN pip install geojson
RUN pip install geojson-rewind
RUN pip install jupytext
RUN pip install black

# Create a directory in the container called notebooks and set it as the working directory
RUN mkdir notebooks
WORKDIR notebooks/

# Copy the local Data folder into the Data folder inside the container
COPY Data/   /notebooks/Data/  

# Create an Out folder inside the Data folder where the output of the notebooks goes to
RUN mkdir /notebooks/Data/Out

# Copy the notebook
COPY Liverpool_map.ipynb  Further_analysis.ipynb   /notebooks/	


# Run the container on container port 8009
CMD ["jupyter", "notebook", "--port=8009", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
