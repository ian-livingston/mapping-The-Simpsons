# For scoring with cross-validation (3-fold) simple linear regression model
def r2_score_lr(X, y, folds=3, loops=5, print_all=False):
    '''
    Parameters:
    -----------
    folds (int): Number of n_splits used by KFold.
    
    loops (int): Number of times to run cross_val_score using a different 
    random state (which begin at 0 and increment up to the value of loops).
    
    print_all: If True, function prints the list of all r2 scores as well. 
    Default value is False.
    
    Returns:
    --------
    Mean r2 score from a list of r2 scores obtained using cross_val_score.
    
    Requires: 
    ---------
    - "import numpy as np"
    - "from sklearn.model_selection import KFold, cross_val_score"
    '''
    
    lr = LinearRegression()
    listed_scores = []
    
    for i in range(loops):
        kf = KFold(n_splits=folds, shuffle=True, random_state=i)
        listed_scores.extend(cross_val_score(lr, X, y, cv=kf, scoring="r2"))
    
    if print_all == True:
        print(listed_scores)
    
    return np.mean(listed_scores)

# For scoring with cross-validation (3-fold) model with PolynomialFeatures
def r2_score_poly(X, y, folds=3, loops=5, degree=2, print_all=False):
    '''
    Parameters:
    -----------
    folds (int): Number of n_splits used by KFold.
    
    loops (int): Number of times to run cross_val_score using a different 
    random state (which begin at 0 and increment up to the value of loops).
    
    degree (int): Degree to be input into PolynomialFeatures. Default value
    is 2.
    
    print_all: If True, function prints the list of all r2 scores as well. 
    Default value is False.
    
    Returns:
    --------
    Mean r2 score from a list of r2 scores obtained using cross_val_score.
    
    Requires: 
    ---------
    - "import numpy as np"
    - "from sklearn.preprocessing import PolynomialFeatures"
    '''
    
    poly = PolynomialFeatures(interaction_only=True)
    X_poly = poly.fit_transform(X)
    lr_poly=LinearRegression()
    listed_scores = []
    
    for i in range(loops):
        kf = KFold(n_splits=folds, shuffle=True, random_state=i)
        listed_scores.extend(cross_val_score(lr_poly, X_poly, y, cv=kf, scoring="r2"))
    
    if print_all == True:
        print(listed_scores)
    
    return np.mean(listed_scores)


# For scoring with cross-validation (3-fold) Lasso-regularized model
def r2_score_lasso(X, y, folds=3, loops=5, print_all=False):
    '''
    Parameters:
    -----------
    folds (int): Number of n_splits used by KFold.
    
    loops (int): Number of times to run cross_val_score using a different 
    random state (which begin at 0 and increment up to the value of loops).
        
    print_all: If True, function prints the list of all r2 scores as well. 
    Default value is False.
    
    Returns:
    --------
    Mean r2 score from a list of r2 scores obtained using cross_val_score.
    
    Requires: 
    ---------
    - "import numpy as np"
    - "from sklearn.preprocessing import StandardScaler"
    - "from sklearn.linear_model import LassoCV"
    '''
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    #alphavec = 10**np.linspace(-1, 1, 100)
    lasso = LassoCV(cv=5)
    listed_scores = []
    
    for i in range(loops):
        kf = KFold(n_splits=folds, shuffle=True, random_state=i)
        listed_scores.extend(cross_val_score(lasso, X_scaled, y, cv=kf, scoring="r2"))
    
    if print_all == True:
        print(listed_scores)
    
    return np.mean(listed_scores)


# For scoring with cross-validation (3-fold) Ridge-regularized model
def r2_score_ridge(X, y, folds=3, loops=5, print_all=False):
    '''
    Parameters:
    -----------
    folds (int): Number of n_splits used by KFold.
    
    loops (int): Number of times to run cross_val_score using a different 
    random state (which begin at 0 and increment up to the value of loops).
        
    print_all: If True, function prints the list of all r2 scores as well. 
    Default value is False.
    
    Returns:
    --------
    Mean r2 score from a list of r2 scores obtained using cross_val_score.
    
    Requires: 
    ---------
    - "import numpy as np"
    - "from sklearn.preprocessing import StandardScaler"
    - "from sklearn.linear_model import RidgeCV"
    '''
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    alphavec = 10**np.linspace(-1, 1, 100)
    ridge = RidgeCV(alphas=alphavec, cv=5)
    listed_scores = []
    
    for i in range(loops):
        kf = KFold(n_splits=folds, shuffle=True, random_state=i)
        listed_scores.extend(cross_val_score(ridge, X_scaled, y, cv=kf, scoring="r2"))
    
    if print_all == True:
        print(listed_scores)
    
    return np.mean(listed_scores)


# For measuring MAE
def mae(y_true, y_pred):
    return np.mean(np.abs(y_pred-y_true))