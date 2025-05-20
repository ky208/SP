FROM tensorflow/serving

WORKDIR /Model_Development
COPY Model_Development/img_classifier/Model1_Large /models/img_classifier/Model1_Large
COPY Model_Development/img_classifier/Model2_Small /models/img_classifier/Model2_Small
COPY Model_Development/models.config /models/models.config

ENV MODEL_CONFIG_FILE=/models/models.config
EXPOSE 8501

CMD ["tensorflow_model_server","--rest_api_port=8501","--model_config_file=/models/models.config"]