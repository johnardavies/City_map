# Miniconda base image
FROM continuumio/miniconda:latest
RUN apt-get update && apt-get install -y libgtk2.0-dev 

# Install python and usefil datascience libraries   
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
# Create a directory in the container notebooks

RUN mkdir notebooks
WORKDIR notebooks/

COPY Data/       /notebooks/Data/  
RUN mkdir /notebooks/Data/Out

# Copy the notebook
COPY Liverpool_map.ipynb  /notebooks/	



# Run the container on container port 8009
CMD ["jupyter", "notebook", "--port=8009", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
