import os, logging
from flask import jsonify, request, Response ,send_file
from pathlib import Path
from services.run_service import save_and_run
from utils import get_uploads_dir
from werkzeug.utils import secure_filename




DEFAULT_AUDIO_FILENAME = "audio.webm"
DEFAULT_VIDEO_FILENAME = "face.webm"
DEFAULT_OUTPUT_FILENAME = "output.mp4"



def init_app(app):
    @app.route("/uploads/<filename>", methods=["GET"])
    def uploaded_file(filename):
        
        filename = secure_filename(filename)
        uploads_dir = get_uploads_dir()
        fullpath = os.path.normpath(os.path.join(uploads_dir, filename))
    
        if not fullpath.startswith(uploads_dir):
            return jsonify(error="Access denied"), 403
        
        try:
            with open(fullpath, "rb") as f:
                file_content = f.read()
            return Response(file_content, content_type="video/webm")
        except FileNotFoundError:
            return jsonify(error="File not found"), 404

    


    @app.route("/api/files", methods=["POST"])
    def files():
        print("request",request)
        print("request files",request.files)
        if "source" not in request.files or "target" not in request.files:
            return jsonify(error="Missing source or target file"), 400
        
        print("files",request.files)
        uploads_dir = get_uploads_dir()
        
        target_file = request.files["target"]
        # print("temp path is",os.path.join(uploads_dir,"anshu1.png"))
        # target_file.save(os.path.join(uploads_dir,"anshu1.png"))
        source_file = request.files["source"]
        print("target is",target_file, type(target_file))

        # Access information:=
        # file_size = len(target_file.read())  # Size in bytes

        # Determine file type:

        if target_file.content_type.startswith('video/'):
            content_type="video"
        elif target_file.content_type.startswith('image/'):
            content_type="image"
        else:
            content_type="unknown"
            print("File type is unknown.")


        

        content_type=target_file.content_type

        try:
            output_path=save_and_run(target_file, source_file)
            if Path(output_path).is_file():
                    response = jsonify(url=os.path.basename(output_path))
                    response.headers['Content-Type'] = content_type
                    print("response is ",response)

                    return (
                        response,
                        200,
                    )
            else:
                    return (
                        jsonify(error="Output file not found."),
                        404,
                    )  



        except Exception as e:
            raise Exception("Error in root route: " + str(e))

       
       


