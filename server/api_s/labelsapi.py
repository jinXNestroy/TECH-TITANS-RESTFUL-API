from flask import request, jsonify
from database import db
from models import Label
from utils import calculate_label_revenue

class LabelAPI:
    @staticmethod
    def create_label():
        data = request.get_json()
        if not data or not data.get('name') or not data.get('type'):
            return jsonify({'error': 'Label name and type are required'}), 400
        
        label = Label(
            name=data['name'],
            type=data['type'],
            flat_rate=data.get('flat_rate', 0.0)  # Optional flat_rate if provided
        )
        db.session.add(label)
        db.session.commit()
        
        return jsonify({
            'id': str(label.id),
            'name': label.name,
            'type': label.type,
            'flat_rate': label.flat_rate
        }), 201

    @staticmethod
    def get_all_labels():
        labels = Label.query.all()
        return jsonify([
            {
                'id': str(label.id),
                'name': label.name,
                'type': label.type,
                'flat_rate': label.flat_rate
            }
            for label in labels
        ])

    @staticmethod
    def get_all_labels_revenue():
        labels = Label.query.all()
        label_revenues = []
        
        for label in labels:
            label_revenue = calculate_label_revenue(label)
            label_revenues.append({
                'label_id': str(label.id),
                'label_name': label.name,
                'revenue': label_revenue
            })
        
        return jsonify(label_revenues)

    @staticmethod
    def get_label_revenue(label_id):
        label = Label.query.get(label_id)
        if not label:
            return jsonify({'error': 'Label not found'}), 404
        
        label_revenue = calculate_label_revenue(label)
        return jsonify({
            'label_id': str(label.id),
            'label_name': label.name,
            'revenue': label_revenue
        })
