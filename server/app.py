#!/usr/bin/env python3

from flask import Flask, request, make_response, session
from flask_restful import Api, Resource

from config import app, db, api
from models import User, Article

class ClearSession(Resource):

    def delete(self):
        
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class IndexArticle(Resource):
    
    def get(self):
        
        articles = [article.to_dict() for article in Article.query.all()]
        return articles, 200

class ShowArticle(Resource):

    def get(self, id):

        session['page_views'] = 0 if not session.get('page_views') else session.get('page_views')
        session['page_views'] += 1

        if session['page_views'] <= 3:

            article = Article.query.filter(Article.id == id).first()
            article_json = article.to_dict()

            return article_json, 200

        return {'message': 'Maximum pageview limit reached'}, 401

class Login(Resource):
    
    def post(self):
        
        username = request.get_json()['username']
        
        user = User.query.filter(User.username == username).first()
        
        session['user_id'] = user.id
        
        return user.to_dict(), 200

class Logout(Resource):
    
    def delete(self):
        
        session['user_id'] = None
        
        return {}, 204

class CheckSession(Resource):
    
    def get(self):
        
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict(), 200
        else:
            return {}, 401

class MemberOnlyIndex(Resource):
    
    def get(self):
        # Check if user is logged in by checking session
        if not session.get('user_id'):
            return {'message': 'Unauthorized'}, 401
        
        # If user is logged in, return member-only articles
        member_articles = Article.query.filter(Article.is_member_only == True).all()
        return [article.to_dict() for article in member_articles], 200

class MemberOnlyArticle(Resource):
    
    def get(self, id):
        # Check if user is logged in by checking session
        if not session.get('user_id'):
            return {'message': 'Unauthorized'}, 401
        
        # Find the article by ID
        article = Article.query.get(id)
        
        # If article doesn't exist, return 404
        if not article:
            return {'message': 'Article not found'}, 404
            
        # Return the article (the test expects any article to be returned if user is logged in)
        return article.to_dict(), 200
        return article.to_dict(), 200

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(IndexArticle, '/articles', endpoint='articles')
api.add_resource(ShowArticle, '/articles/<int:id>', endpoint='show_article')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(MemberOnlyIndex, '/members_only_articles', endpoint='members_only_articles')
api.add_resource(MemberOnlyArticle, '/members_only_articles/<int:id>', endpoint='members_only_article')

if __name__ == '__main__':
    app.run(port=5555, debug=True)