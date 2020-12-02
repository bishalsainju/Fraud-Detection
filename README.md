Fraud Detection
In this project we used various predictive models to see how accurate they are in detecting whether a
transaction is a normal payment or a fraud. The features provided were already scaled and the names of the
features were not shown due to privacy reasons. Only 2 features are not scaled, time and amount.
Main Objective of this project is:
  1. Learning to deal with imbalanced datasets?
  2. Implementing various techniques like Random Under Sampling method to balance the unbalanced
  datasets.
  3. Building models on the basis of various classifiers (Logistic Regression and SVM) and figuring out which
  classifier works the best.
  4. Seeing if model built from Undersampling method generalize well in whole of the dataset.

For analysis we used Logistic Regression and SVC classifier.
We have found quite an interesting result that, when model is build from the subset of the original sample, since
there are a lot of fraud classes in the undersample, which is generally not the case in real life, where most of the
transactions are non-fraud, and because we built the model from subsample, where this property is violated, we
get a model, which is biased towards frauds, i.e., it will predict most of the non-fraud transactions fraud, which
is a problem, as the model that we build from this sub-sample does not quite work well with unseen data.
So, this might be a problem with the model that we created.

Religion & Philosophy
The purpose of this analysis is to determine the predictive power of a historical society's religious configuration
for whether or not the society developed a system of philosophy. This is a potentially useful metric for
translators of ancient texts, as knowing the likely contexts of a given untranslated text can be very helpful for
translation.
