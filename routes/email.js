"use strict"

const articledb = require('../models/ArticleDB');
var articleDBObject = new articledb();

function routeArticles(app){
    app.route('/articles')
    .get(articleDBObject.getAllArticles)
    .post(articleDBObject.addArticle);
    app.route('/articles/:article_id')
    .put(articleDBObject.updateArticle)
    .delete(articleDBObject.deleteArticle);
    }
    



        

module.exports = {routeArticles};