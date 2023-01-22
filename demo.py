from Thyroid.pipeline.pipeline import Pipeline
from Thyroid.exception import ThyroidException
from Thyroid.logger import logging
def main():
    try:
        logging.info('Starting the pipeline...')
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")
        print(e)
    

if __name__ == '__main__':
    main()

