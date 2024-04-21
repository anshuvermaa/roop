import os
from services.faceswap_inference import run_faceswap_inference
from utils import get_uploads_dir





def clean_files(target_path, source_path):
    if os.path.exists(target_path):
        os.remove(target_path)
    if os.path.exists(source_path):
        os.remove(source_path)


def save_and_run(target_file, source_file):
    uploads_dir = get_uploads_dir()
    try:
        try:
                target_fileName = target_file.filename
                source_fileName = source_file.filename
                target_path = os.path.join(uploads_dir,target_fileName)
                source_path = os.path.join(uploads_dir,source_fileName)

                target_file.save(target_path)
                source_file.save(source_path)
        except Exception as e:
              raise Exception("Error: something went wrong with saving files " + str(e))
        
        
        file = os.path.splitext(target_path)[0]
        print("file is",file)
        output_path = os.path.join(get_uploads_dir(),"outputs",file+"_output"+os.path.splitext(target_path)[1])
        print("output_path is",output_path)

        run_faceswap_inference(
            source_path=source_path, target_path=target_path, outfile_path=output_path
        )
    except Exception as e:
        # clean_files(target_path, source_path)
        raise Exception("Error: " + str(e))

    return output_path
