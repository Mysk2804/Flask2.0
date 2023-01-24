from flask import Flask, jsonify, request
from flask.views import MethodView
from database import Session, AdvertisementModel
from sqlalchemy.exc import IntegrityError
from errors import HttpException

app = Flask('app')


@app.errorhandler(HttpException)
def error_handler(error: HttpException):
    http_response = jsonify({
        'status': 'error',
        'message': error.message
    })
    http_response.status_code = error.status_code
    return http_response


def get_advertisement(advertisement_id: int, session: Session) -> AdvertisementModel:
    advertisement = session.query(AdvertisementModel).get(advertisement_id)
    if advertisement is None:
        raise HttpException(
            status_code=404,
            message='advertisement not fount'
        )
    return advertisement


class Advertisement(MethodView):

    def get(self, advertisement_id):
        with Session() as session:
            advertisement = get_advertisement(advertisement_id, session)

            return jsonify({
                'id': advertisement.id,
                'advertisement': advertisement.title,
                'creation_time': advertisement.date_of_creation.isoformat(),
                'owner': advertisement.owner
            })

    def post(self):
        advertisement_data = request.json
        with Session() as session:
            new_advertisement = AdvertisementModel(**advertisement_data)
            session.add(new_advertisement)
            try:
                session.commit()
            except IntegrityError:
                raise HttpException(
                    status_code=409,
                    message='there is an advertisement with this title')
            return jsonify({'id': new_advertisement.id,
                            'title': new_advertisement.title})

    def patch(self, advertisement_id: int):
        json_data = request.json
        with Session() as session:
            advertisement = get_advertisement(advertisement_id, session)
            for field, value in json_data.items():
                setattr(advertisement, field, value)
            session.add(advertisement)
            session.commit()
            return jsonify({'status': 'success'})


    def delete(self, advertisement_id: int):
        with Session() as session:
            advertisement = get_advertisement(advertisement_id, session)
            session.delete(advertisement)
            session.commit()
            return jsonify({'status': 'success'})


app.add_url_rule('/advertisement/<int:advertisement_id>',
                 view_func=Advertisement.as_view('advertisement'),
                 methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/advertisement/', view_func=Advertisement.as_view('create_advertisement'), methods=['POST'])


if __name__ == '__main__':
    app.run()
