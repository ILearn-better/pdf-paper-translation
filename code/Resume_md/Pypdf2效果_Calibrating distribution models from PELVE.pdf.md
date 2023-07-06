arXiv:2204.08882v4  [q-fin.RM]  29 Jun 2023Calibrating distribution models from PELVE
Hirbod Assa∗Liyuan Lin†Ruodu Wang‡
June 30, 2023
Abstract
The Value-at-Risk (VaR) and the Expected Shortfall (ES) are the two most popular risk mea-
sures in banking and insurance regulation. To bridge betwee n the two regulatory risk measures, the
Probability Equivalent Level of VaR-ES (PELVE) was recentl y proposed to convert a level of VaR
to that of ES. It is straightforward to compute the value of PE LVE for a given distribution model.
In this paper, we study the converse problem of PELVE calibra tion, that is, to ﬁnd a distribution
model that yields a given PELVE, which may either be obtained from data or from expert opinion.
We discuss separately the cases when one-point, two-point, n-point and curve constraints are given.
In the most complicated case of a curve constraint, we conver t the calibration problem to that of
an advanced diﬀerential equation. We apply the model calibr ation techniques to estimation and
simulation for datasets used in insurance. We further study some technical properties of PELVE
by oﬀering a few new results on monotonicity and convergence .
Keywords: Value-at-Risk, Expected Shortfall, risk measures, heavy tails, ad vanced diﬀerential
equation.
1 Introduction
Value-at-Risk (VaR) and Expected Shortfall (ES, also known as TV aR and CVaR) are the most
widely used risk measures for regulation in ﬁnance and insurance. Th e former has gained its popularity
due to its simplistic approachtowardriskas the riskquantile, and the second one is perceived to be use-
ful as a modiﬁcation of VaR with more appealing properties, such as t ail-sensitivity and subadditivity,
as studied in the seminal work of Artzner et al. (1999).
In the Fundamental Review of the Trading Book (FRTB), the Basel Committee on Banking Su-
pervision ( BCBS(2019)) proposed to replace VaR at 1% conﬁdence with ES with a 2.5% conﬁd ence
∗Kent Business School, UK. h.assa@kent.ac.uk .
†Department of Statistics and Actuarial Science, Universit y of Waterloo, Canada. l89lin@uwaterloo.ca .
‡Department of Statistics and Actuarial Science, Universit y of Waterloo, Canada. wang@uwaterloo.ca .
1interval for the internal model-based approach.1The main reason, as mentioned in the FRTB, was that
ES can better capture tail risk; see Embrechts et al. (2018) for a concrete risk sharing model where tail
risk is captured by ES and ignored by VaR. On the other hand, VaR als o has advantages that ES does
not have, such as elicitability (e.g., Gneiting (2011) andKou and Peng (2016)) or backtesting tractabil-
ity (e.g., Acerbi and Sz´ ekely (2014)), and the two risk measures admit diﬀerent axiomatic foundations
(seeChambers (2009) andWang and Zitikis (2021)). We refer to the reviewsof Embrechts et al. (2014)
andEmmer et al. (2015) for general discussions on VaR and ES, and McNeil et al. (2015) for a stan-
dard treatment on risk management including the use of VaR and ES. The technical contrasts of the
two risk measures and their co-existence in regulatory practice giv e rise to great interest from both
researchers and practitioners to explore the relationship betwee n them.
TounderstandthebalancingpointofVaRandESduringthetransitio nintheFRTB, Li and Wang
(2022) proposed the Probability Equivalent Level of VaR-ES (PELVE). Th e value of PELVE is the
multiplier to the tail probability when replacing VaR with ES such that th e capital calculation stays
unchanged. Moreprecisely, thePELVEof Xatlevelεisthemultiplier csuchthatES cε(X) = VaR ε(X);
suchcuniquely exists under mild conditions. For instance, if VaR 1%(X) = ES 2.5%(X) for a future
portfolio loss X, then PELVE of Xat probability level 0.01 is the multiplier 2 .5. In this case, replacing
VaR1%with ES 2.5%in FRTB does not havemuch eﬀect on the capital requirement for th e bank bearing
the lossX. Instead, if ES 2.5%(X)>VaR1%(X), then the bank has a larger capital requirement under
the new regulatory risk measure; this is often the case for ﬁnancia l assets and portfolios as shown by
the empirical studies in Li and Wang (2022). The PELVE enjoys many convenient properties, and it
has been extended in a few ways. In particular, Fiori and Rosazza Gianin (2023) deﬁned generalized
PELVE by replacing VaR and ES with another pair of monotone risk mea sures (ρ,˜ρ), andBarczy et al.
(2022) extended PELVE by replacing ES with a higher-order ES.
For a given distribution model or a data set, its PELVE can be comput ed or estimated in a
straightforward manner. As argued by Li and Wang (2022), the PELVE for a small εmay be seen
as a summarizing index measuring tail heaviness in a non-limit sense. As such, one may like to
generate models for a given PELVE, in a way similar to constructing mo dels for other given statistical
information; see e.g., Embrechts et al. (2002,2016) for constructing multivariate models with a given
correlation or tail-dependence matrix. Such statistical informatio n may be obtained either from data
or from expert opinion, but there is no a priori guarantee that a co rresponding model exists. Since
PELVE involves a parameter ε∈(0,1), its information is represented by a curve. The calibration
problem, that is, to ﬁnd a distribution model for given PELVE values o r a given PELVE curve, turns
out to be highly non-trivial, and it is the main objective of the current paper.
From now on, suppose that we receive some information on the PELV E of a certain random
1In this paper, we use the “small α” convention for VaR and ES. Hence, “VaR at 1% conﬁdence” and “ ES at 2.5%
conﬁdence” correspond to VaR 99%and ES 97.5%inBCBS(2019), respectively.
2loss from an expert opinion, and we aim to build a distribution model con sistent with the supplied
information. Since PELVE is location-scale invariant, such a distribut ion, if it exists, is not unique.
The calibration problem is trivial if we are supplied with only one point on t he PELVE curve.
As the PELVE curve of the generalized Pareto distribution is a const ant when the PELVE is well
deﬁned, we can use the generalized Pareto distribution to match th e given PELVE value, which has
a tail index implied from the expert opinion. The calibration problem bec omes more involved if we
are supplied with two points on the PELVE curve, because the value o f the PELVE at two diﬀerent
probability levels interact with each other. The situation becomes mo re complicated as the number of
points increases, and we further turn to the problem of calibration from a fully speciﬁed PELVE curve.
Calibrating distribution from the PELVE curve can be reformulated a s solving for a function fvia the
integral equation/integraltexty
0f(s)ds=yf(z(y)y), where the curve zis computed from the PELVEcurve. This
integralequation can be further convertedto an advanceddiﬀer ential equation(see Bellman and Cooke
(1963)). For the case that zis a constant curve, we can explicitly obtain all solutions for f. We ﬁnd
other distributions that also have constant PELVE curves other t han the simple ones with a Pareto or
exponential distribution. As a consequence, a PELVE curve does n ot characterize a unique location-
scale family of distributions; this providesa negativeanswerto a que stion posed by Li and Wang (2022,
Section 7, Question (iv)). For general function z, we develop a numerical method to compute f.
The calibrated distribution can be used to estimate the value of othe r risk measures such as VaR
and ES at diﬀerent levels. We illustrate by an empirical example that tw o points of PELVE give a
quite good summary of the tail distribution of risk. Daily log-losses (n egative log-returns) of Apple
(AAPL) from Yahoo Finance are collected for the period from Janua ry 3, 2012 to December 31, 2021
within total of 2518 observations. We calculate the empirical PELVE at levels 0.01 and 0.05 using the
empirical PELVE estimator provided by Li and Wang (2022, Section 5) with a moving window of 500
trading days. For each pair of two points of PELVE at levels 0.01 and 0 .05, we produce a quantile
curve from the two empirical PELVE points by our calibration model in Section3.2, which is scaled
such that VaR 0.01and VaR 0.05are equal to their empirical values.2Figure1presents the empirical and
calibrated quantile curves on December 31, 2021 using 500 trading d ays prior to that date. The two
quantile curves are close to each other, with our calibrated curve b eing more smooth. We also report
the values of ES 0.025of the calibrated distribution, which we call the calibrated ES 0.025, and compare it
with empirical ES 0.025. The left panel of Figure 2shows the curves of empirical and calibrated ES 0.025.
In the right panel of Figure 2, we create a scatter plot using empirical and calibrated ES 0.025. Both
ﬁgures show that the empirical and calibrated ES 0.025curves are quite close.
To further enrich the theory of PELVE, we study a few technical p roperties of PELVE, such as
monotonicity and convergence as the probability level goes to 0. A d ecreasing PELVE indicates a
2Recall that PELVE is location-scale free, and hence we need t o pick two free parameters to specify a distribution
calibrated from PELVE.
3Figure 1: Empirical VaR and calibrated VaR
0 0.02 0.04 0.06 0.08 0.1 0.12 0.14 0.16
Log loss00.020.040.060.080.10.120.140.16
Empirical VaR
Calibrated VaR
Figure 2: Empirical ES 0.05and calibrated ES 0.05
2014 2015 2016 2017 2018 2019 2020 2021 2022 2023
Year0.030.0350.040.0450.050.0550.060.0650.070.0750.08
0.03 0.04 0.05 0.06 0.07 0.08 0.090.030.040.050.060.070.080.09
relatively larger impact of ES in risk assessment than VaR moving towa rds the tail. As we will see,
while for the most known parametric distributions the PELVE is decre asing, there exist some examples
at some risk levels it is not decreasing. This means that for those exa mples VaR becomes a stricter
risk measure when moving towards the tail. To obtain conditions for m onotonicity, we deﬁne the
dual PELVE by moving the multiplier cfrom the ES side to the VaR side. PELVE can be seen as a
functional measure of tail heaviness in the sense that a heavier-t ailed distribution has a higher PELVE
curve (Li and Wang (2022, Theorem 1)). The hazard rate, on the other hand, is another fu nctional
measure of tail heaviness. We show that the PELVE is decreasing (in creasing) if the inverse of the
hazard rate is convex (concave). Monotonicity also leads to condit ions for the PELVE to have a limit
at the tail, which from the risk management perspective, identiﬁes t he ultimate relative positions of
ES and VaR in the tail region. From a mathematical perspective, the limit of PELVE at 0 allows us
to extend the domain of PELVE to include 0 as a measure of tail heavin ess.
4The rest of this paper is organized as follows. Section 2introduces the background and examples
of the PELVE. In Section 3we calibrate a distribution from ﬁnitely many points in the PELVE curve .
Section4calibratesthedistributionfromgivenPELVEcurves,wherewegivea classofexplicitsolutions
for constant PELVE functions and numerical solutions for genera l PELVE functions. In Section 5, we
study the monotonicity and convergence of the PELVE. Section 6presents two examples of the model
calibration techniques applied to datasets used in insurance. A conc lusion is given in Section 7. Some
technical proofs of results in Sections 3,4and5are provided in the Appendices.
2 Deﬁnitions and background
Let us consider an atomless probability space (Ω ,F,P), where Fis the set of the measurable sets
andPis the probability measure. Let L1be the set of integrable random variables, i.e., L1={X:
E[|X|]<∞}, whereEis the expectation with respect to P.
We ﬁrst deﬁne VaR and ES in L1, the two most popular risk measures. The VaR at probability
levelp∈(0,1) is deﬁned as
VaRp(X) = inf{x∈R:P(X/lessorequalslantx)/greaterorequalslant1−p}=F−1(1−p), X∈L1, (1)
whereFis the distribution of X. The ES at probability level p∈[0,1) is deﬁned as
ESp(X) =1
p/integraldisplayp
0VaRq(X)dq, X∈L1.
Note that we use the “small α” convention for VaR and ES, which is diﬀerent from Liu and Wang
(2021). Let VaR 0(X) = ES 0(X) = ess-sup( X) and VaR 1(X) = ess-inf( X). We have that ES 1(X) is
the mean of X. We will also call p/ma√sto→VaRp(X) the quantile function of X, keeping in mind that in
our convention this function is decreasing.3
Forε∈(0,1), the PELVE at level ε, proposed by Li and Wang (2022), is deﬁned as
ΠX(ε) = inf{c∈[1,1/ε] : EScε(X)/lessorequalslantVaRε(X)}, X∈L1,
where inf( ∅) =∞.Li and Wang (2022) used Π ε(X) for our Π X(ε), and our choice of notation is due
to the fact that the curve ε→ΠX(ε) is the main quantity of interest in this paper.
ThePELVEof Xisﬁnite ifandonlyifVaR ε(X)/greaterorequalslantE[X]. Thevalue ofthePELVEisthe multiplier
csuch that ES cε(X) = VaR ε(X).If VaR p(X) is not a constant for p∈(0,ε], then the PELVE is the
unique solution for the multiplier. By Theorem 1 in Li and Wang (2022), the PELVE is location-scale
3Throughout the paper, all terms like “increasing” and “decr easing” are in the non-strict sense.
5invariant. The distribution with a heavy tail will have a higher PELVE va lue.
IfXis a normal distributed random variable and ε= 1%, we have Π X(ε)≈2.5. It means that
ES2.5%(X)≈VaR1%(X). That is, the replacement suggested by BCBS is fair for normally dis tributed
risks. In other words, a higher PELVE will result in a higher capital re quirement after the replacement.
In this paper, we are generally interested in the question of which dis tributions have a speciﬁed
or partially speciﬁed PELVE curve. We ﬁrst look at a few simple example s.
Example 1 (Constant PELVE) .We ﬁrst list some distributions that have constant PELVE curves.
From the deﬁnition of the PELVE, we know that the PELVE should be la rger than 1. As we can
see from Table 1, the PELVE for the generalized Pareto distribution takes values on (1,∞). For
X∼GPD(ξ), we have 1 <ΠX(ε)< ewhenξ <0, ΠX(ε) =ewhenξ= 0 and Π X(ε)> ewhen
ξ >0. Furthermore, if Xfollows the point-mass distribution δcor the Bernoulli distribution, we have
ΠX(ε) = 1.
Table 1: Example of constant PELVE
Distribution Distribution or probability function of X ΠX(ε)
δc P(X=c) = 1 ΠX(ε) = 1 for ε∈(0,1)
B(1,p) P(X= 1) =pandP(X= 0) = 1 −p ΠX(ε) = 1 for ε∈(0,p)
U(0,1) F(t) =tfort∈(0,1)ΠX(ε) = 2 for
0< ε <1/2
EXP(λ) F(t) = 1−exp(−λt), λ >0ΠX(ε) =efor
0< ε <1/e
GPD(ξ)1F(x) =/braceleftBigg
1−(1+ξx)−1
ξξ/ne}ationslash= 0
1−exp(−x)ξ= 0ΠX(ε) = (1−ξ)−1
ξfor
0< ε <(1−ξ)1
ξ
1The distribution GPD( ξ) is called the standard generalized Pareto distribution. A sE[X]<∞whenξ <1,
the PELVE exists only when ξ <1. The support of GPD( ξ) is [0,∞) whenξ >0 and [0,−1
ξ] whenξ <0.
Whenξ= 0, the GPD( ξ) is exactly exponential distribution with λ= 1/σ. There is a three-parameter
GPD(µ,σ,ξ), which is a location-scale transform of standard GPD. Ther efore, GPD( µ,σ,ξ) has the same
PELVE as GPD( ξ).
Example 2. Herewepresentsomenon-constantPELVEexamples. We writet( v) forthe t-distribution
with parameter (0 ,1,v), and LN( σ) for the log-normal distribution with parameter (0 ,σ2). As we can
see, for normal distribution and t-distribution, the PELVE curve is decreasing as εincreasing. The
monotonicity of the PELVE of the lognormal distribution depends on the value of σ. The monotonicity
of the PELVE will be further discussed in Section 5. For more PELVE examples, see Li and Wang
(2022).
6Figure 3: PELVE for normal distribution, t-distribution and lognorm al distribution
0 0.02 0.04 0.06 0.08 0.1 0.12 0.14 0.16 0.18 0.22.352.42.452.52.552.6PELVEN(0,1)
0 0.02 0.04 0.06 0.08 0.1 0.12 0.14 0.16 0.18 0.22.72.82.933.13.23.33.4PELVEt(2)
0 0.02 0.04 0.06 0.08 0.1 0.12 0.14 0.16 0.18 0.22.42.52.62.72.82.933.13.23.3PELVELognormal
LN(1)
LN(0.2)
3 Calibration from ﬁnite-point constraints
In this section, we discuss the calibration problem when some points o f the PELVE are given. We
will focus on the case where one point or two points on the PELVE cur ve are speciﬁed, for which we
can explicitly construct a corresponding quantile function.
Weﬁrstnotethatthecalibrateddistributionisnotunique. Forexam ple,ifwearegivenΠ X(0.01) =
2.5, we can assume the distribution of Xis the Normal distribution or the generalized Pareto distri-
bution with tail parameter ξsatisfying (1 −ξ)−1/ξ= 2.5 from Table 1. Therefore, the distributions
obtained in our results are only some possible choices, which we choos e to have a generalized Pareto
tail, as Pareto tails are standard in risk management applications.
3.1 Calibration from a one-point constraint
Based on Table 1, we can calibrate the distribution for Xfrom one given PELVE point ( ε1,c1)
such that Π X(ε1) =c1. A simple idea is to take the generalized Pareto distribution when c1>1 and
δcwhenc1= 1. We summarize the idea in the following Proposition.
Proposition 1. Letε1∈(0,1)andc1∈[1,∞)such that c1ε1/lessorequalslant1. Ifc1>1, letξ∈Rsuch that
(1−ξ)−1
ξ=c1. Then,X∼GPD(ξ)hasΠX(ε1) =c1. Ifc1= 1, thenX=kfor some constant k∈R
hasΠX(ε1) =c1.
7The proof can be directly derived from Table 1and it is omitted. By Proposition 1, if we have
the value of PELVE at point ε1, we can ﬁnd a distribution of Xwhich has the same PELVE value at
ε1. If we also have the value of VaR at ε1, we can determine the scale parameter ( σ) for the GPD
distribution or the value of kto match the value of VaR. For Table 1, we can see that the calibrated
generalized Pareto distribution can also serve as a solution for a mor e prudent condition Π X(ε)/greaterorequalslantc1
whenε∈(0,ε1).
3.2 Calibration from a two-point constraint
The calibration problem would be much more diﬃcult when we are given tw o points ofthe PELVE
curve. Given two points ( ε1,c1) and (ε2,c2) such that ε1< ε2, we want to ﬁnd a distribution for
X∈L1such that Π X(ε1) =c1and Π X(ε2) =c2. Nevertheless, the choices of ( ε1,c1) and (ε2,c2) are
not arbitrary. First, we need 1 /lessorequalslantc1/lessorequalslant1/ε1and 1/lessorequalslantc2/lessorequalslant1/ε2by the deﬁnition of the PELVE. Then,
we will show that the value of c2will be restricted if ( ε1,c1) andε2are given.
Lemma 1. For any X∈L1, letε1,ε2∈(0,1)be such that E[X]/lessorequalslantVaRε2(X)andε1< ε2. Then, we
haveε1ΠX(ε1)/lessorequalslantε2ΠX(ε2).
By Lemma 1, for given ε1,ε2andc1, the value of c2is bounded below by both 1 and c1ε1/ε2. We
also note that if c2= 1, then p/ma√sto→VaRp(X) is constant on (0 ,ε2), which implies c1= 1. In Appendix
A, Proposition 6shows that the above lower bound is achieved if and only if VaR ε1(X) = VaR ε2(X).
From the deﬁnition of the PELVE and Lemma 1, forε1< ε2, the possible choices of ( ε1,c1) and
(ε2,c2) should satisfy 1 /lessorequalslantc1/lessorequalslant1/ε1, 1/lessorequalslantc2/lessorequalslant1/ε2andc1ε1/lessorequalslantc2ε2. We denote by ∆ the admissible
set for (ε1,c1,ε2,c2), that is,
∆ ={(ε1,c1,ε2,c2)∈((0,1)×[1,∞))2:ε1< ε2, c1ε1/lessorequalslant1, c2ε2/lessorequalslant1, c1ε1/lessorequalslantc2ε2}.
We illustrate the possible region of ( c1,c2) with given ε1andε2in Figure 4. We divide the region into
5 cases and calibrate the distribution for each case.
The calibration process is to construct a continuous and decreasin g quantile function that can
satisfy two equivalent conditions between VaR and ES, which are
ESc1ε1(X) = VaR ε1(X) and ES c2ε2(X) = VaR ε2(X). (2)
As we can see, only the values of VaR ε(X) forε∈(0,c2ε2] matters for the equivalent condition ( 2).
Therefore, we focus on constructing VaR ε(X) forε∈(0,c2ε2]. In addition, we want a continuous
calibrated quantile function.
The case c1= 1 orc2= 1 is special, which means that VaR ε(X) is a constant on the tail part. If
8Figure 4: Admissible region of ( c1,c2)
c2
c1 1 1/ε111/ε2
ε2/ε1•
Case 1Case 2
Case 3Case 4Case 5
c1>1, we can set the tail distribution as the generalized Pareto distribu tion from Table 1such that
ΠX(ε1) =c1.
Forz= (ε1,c1,ε2,c2)∈∆, we will construct a class of functions, denoted by Gz, in ﬁve diﬀerent
cases according to Figure 4. The function t/ma√sto→Gz(t) will be our desired quantile function. If c1= 1, let
ˆk,˜k∈Rbe any two constants satisfying ˜k <ˆk. Ifc1>1, letξ∈(−∞,1) be such that (1 −ξ)−1/ξ=c1,
k(ε) =

1
ξ(ε−ξ−1), ξ/ne}ationslash= 0,
−log(ε), ξ= 0,
andk=/integraltextε1
0k(ε)dε. We ﬁrst claim that the function Gzcan be anyarbitrarycontinuousand decreasing
function on [ c2ε2,1) since the values of VaR t(X) fort∈[c2ε2,1) do not aﬀect its PELVE at ε1andε2.
The value of Gzon (0,c2ε2] is given by
(i) Case 1 ,c2= 1 (which implies c1= 1):Gz(ε) =ˆk;
(ii) Case 2 ,c1= 1 and 1 < c2/lessorequalslant1/ε2:
Gz(ε) =

ˆk, ε ∈(0,ε1),
a1ε+b1, ε∈[ε1,ε2),
a2ε+b2, ε∈[ε2,c2ε2],where

a1=˜k−ˆk
ε2−ε1,
b1=ˆk−a1ε1,
a2=(˜k−ˆk)(ε1+ε2)
(c2ε2−ε2)2,
b2=˜k−a2ε2;
9(iii) Case 3 ,ε2/ε1< c1/lessorequalslant1/ε1andc2=c1ε1/ε2:
Gz(ε) =

k(ε), ε ∈(0,ε1),
k(ε1), ε∈[ε1,ε2),
aε+b, ε∈[ε2,c2ε2],where

a=2(k(ε1)ε1−k)
(c2ε2−ε2)2,
b=k(ε1)−aε2;
(iv) Case 4 , 1< c1/lessorequalslantε2/ε1and 1< c2/lessorequalslant1/ε2:
Gz(ε) =

k(ε), ε ∈(0,c1ε1),
a1ε+b1, ε∈[c1ε1,ε2),
a2ε+b2, ε∈[ε2,c2ε2],where

a1=−(c1ε1)−ξ−1,
b1=k(c1ε1)−a1c1ε1,
a2=a1(ε2
2−(c1ε1)2)+2(k(c1ε1)−k(ε1))c1ε1
(c2ε2−ε2)2,
b2=a1ε2+b1−a2ε2;
(v) Case 5 ,ε2/ε1< c1/lessorequalslant1/ε1andc1ε1/ε2< c2/lessorequalslant1/ε2:
Gz(ε) =

k(ε), ε ∈(0,ε1),
a1ε+b1, ε ∈[ε1,ε2),
a1ε2+b1, ε∈[ε2,c1ε1),
a2ε+b2, ε∈[c1ε1,c2ε2],where

a1=k(ε1)ε1−k
(ε2−ε1)(c1ε1−1/2(ε1+ε2)),
b1=k(ε1)−a1ε1,
a2=2c1ε1(a1ε2+b1−k(ε1))
(c1ε1−c2ε2)2,
b2=a1ε2+b1−a2c1ε1.
An illustration of the functions Gzon [0,c2ε2] in Case 2 to Case 5 is presented in Figure 5, and
we omit Case 1 in which Gzis a constant function on [0 ,c2ε2].
Theorem 1. Forz= (ε1,c1,ε2,c2)∈∆, the random variable Xwith a continuous quantile function
given by t/ma√sto→VaRt(X) =Gz(t)satisﬁes ΠX(ε1) =c1andΠX(ε2) =c2.
Remark 1.As we can see from Figure 5, some parts of the calibrated quantile function may be ﬂat,
corresponding to the existence of atoms in the distribution. This ma y be considered as undesirable
from a modeling perspective, and indeed it is forced by the boundary cases of ( ε1,c1,ε2,c2)∈∆ in
Figure4. The ﬂat parts in Cases 1 to 3 are necessary due to Propositions 6. On the other hand,
the ﬂat part in Case 5 can be replaced by a strictly decreasing funct ion. For instance, we can replace
the ﬂat part with a strictly decreasing linear segment as long as c2satisﬁes the bounds shown in
Propositions 7in Appendix A. Another way is to set VaR ε(X) ask(ε) forε∈(0,c1ε1) ifc2/lessorequalslant/parenleftBig
c1ε1(ε−ξ
1−(c1ε1)−ξ)/parenrightBig
//parenleftBig
ε−ξ
2−(c1ε1)−ξ/parenrightBig
, and this choice is applied in the numerical examples in the
Introduction and Section 6. The interested reader can see Propositions 6and7in Appendix A, where
10Figure 5: An illustration of Gzin cases 2 to 5
0 ε1ε2c2ε2Gz(ε)
Gz(ε1)
(a)The function Gzin Case 20 ε1ε2c2ε2Gz(ε)
Gz(ε1)
Gz(ε2)
(b)The function Gzin Case 3
0 ε1c1ε1ε2c2ε2Gz(ε)
Gz(ε1)
(c)The function Gzin Case 40 ε1ε2c1ε1c2ε2Gz(ε)
Gz(c1ε1)
Gz(ε2)
(d)The function Gzin Case 5
we show that a strictly decreasing quantile function cannot attain t he boundary cases ( ε1,c1,ε2,c2),
and hence the ﬂat parts are necessary to include and unify these c ases.
We can easily get the distribution of Xfrom VaR ε(X). As the PELVE is scale-location invariant,
we can scale or move the distribution we get to match more informatio n. For example, if VaR ε1(X)
and VaR ε2(X) are given, we can choose two constants λandµsuch that λX+µmatches the speciﬁed
VaR values. In a similar spirit, the calibration problem can be extended to calibrate the distributions
from some given ES and VaR values. The two points calibration problem can be regarded as given
two ES and VaR values. Calibrating from only ES or VaR would be easy. H owever, the choices of ES
values will also be limited by VaR values if we consider them at the same tim e, which is the same as
the choice of c1,c2as we discussed in this section.
113.3 Calibration from an n-point constraint
As we see above, the PELVE calibration problem is quite technical eve n when only two points on
the PELVE curve are given. By extending the constraint to more th an two points, the problem will in
general become much more complicated. We brieﬂy discuss this prob lem in this section.
For then-point constraint problem, we ﬁrst need to ﬁgure out the admissible set for (εi,ci)i=1,...,n.
By Lemma 1, the admissible set for the n-point calibration problem is a subset of
{(εi,ci)i=1,...,n: 0< ε1<···< εn<1, c1,...,c n/greaterorequalslant1,0< c1ε1/lessorequalslant.../lessorequalslantcnεn/lessorequalslant1}.
However, it is not clear whether each point in the above set is admissib le. There are other constraints
for the admissible points such as Proposition 7. Once the admissible set is determined, we need to
divide the admissible set according to the position of εiandciεi,i= 1,...,n. Furthermore, the case
ci= 1 and ciεi=cjεjfori,j= 1,...,nneed special attention as Cases 1, 2 and 3 in the two-point
constraint problem. For instance, in the three-point constraint p roblem, we need to discuss over 10
separate cases.
Below, we only discuss some special cases of ( εi,ci)i=1,...,n. First, if cn= 1, then the problem
becomes trivial, as the calibrated quantile functions satisfy VaR t(X) =ˆkfor some ˆk∈Rin [0,cnεn].
For the case ckεk> εk/greaterorequalslantck−1εk−1fork= 3,...,n, we can set the calibrated quantile function in
(0,cnεn] recursively. This is because such a conﬁguration of ( εi,ci)i=1,...,nallows for separation of the
constraints, in the sense that we can adjust the values of VaR tfort∈[εk,ckεk] to match PELVE at
εkwithout disturbing VaR tfort/lessorequalslantck−1εk−1. Let VaRk
t(X) be the calibrated quantile function from
thek-point constraint problem for k= 2,...,nwhere VaR2
t(X) follows Theorem 1. The calibrated
quantile function for the n-point constraint problem is
VaRk
t(X) =

VaRk−1
t(X), t∈[0,ck−1εk−1],
ak−1t+bk−1, t∈(ck−1εk−1,εk],
akt+bk, t ∈(εk,ckεk],where

ak=ak−1(ε2
k+c2
k−1ε2
k−1−2ck−1ε2
k−1)
(ckεk−εk)2,
bk=ak−1εk+bk−1−akεk.
In particular, for n= 3, and assuming c3ε3> ε3/greaterorequalslantc2ε2, the calibrated function is given by, with
12z= (ε1,c1ε1,ε2,c2ε2)∈∆,
VaRt(X) =

Gz(t), t ∈[0,c2ε2],
a2t+b2, t∈(c2ε2,ε3],
a3t+b3, t∈(ε3,c3ε3],where

a2=a1(ε2
2−(c1ε1)2)+2(k(c1ε1)−k(ε1))c1ε1
(c2ε2−ε2)2,
b2=−(c1ε1)−ξ−1(ε2−c1ε1)−k(c1ε1)
a3=a2(ε2
3+c2
2ε2
2−2c2ε2
2)
(c3ε3−ε3)2,
b3=a2ε3+b2−a3ε3.
In Figure 6, we show the calibrated quantile function for the case ( ε1,ε2,ε3) = (0.005,0.025,0.1) and
(c1,c2,c3) = (4,3,2.5). Note that the condition c2ε2/lessorequalslantε3is needed here.
Figure 6: Calibrated quantile function when ( ε1,ε2,ε3) = (0.005,0.025,0.1)and (c1,c2,c3) = (4,3,2.5)
0.005 0.025 0.075 0.1 0.25-100-50050
Although we cannot solve the n-point constraint problem in general, we can instead discuss cali-
bration from a given PELVE curve, which is the problem addressed in t he next section.
4 Calibration from a curve constraint
By the location-scale invariance properties of the PELVE, we know t hat the solution cannot be
unique. Conversely, it would be interesting to ask whether all solutio ns can be linearly transformed
from a particular solution; that is, for a given function ε/ma√sto→Π(ε), whether the set {X∈ X: ΠX= Π}is
a location-scale class. This question, as well as identifying Xsatisfying Π X= Π, is the main objective
of this section.
4.1 PELVE and dual PELVE
First, we note that calibrated distributions from an entire PELVE cu rveε/ma√sto→Π(ε) on (0,1) would
be unnatural, because the existence of the PELVE requires E[X]/lessorequalslantVaRε(X) which may not hold for ε
13not very small. Thus, the PELVE curve Π Xdoes not behave well on some parts of (0 ,1). To address
this issue, we introduce a new notion called the dual PELVE and an inte gral equation which can help
us to calibrate the distribution by diﬀerential equations. The dual P ELVE is deﬁned by moving the
multiplier in PELVE from the ES side to the VaR side.
Deﬁnition 1. ForX∈L1, the dual PELVE function of Xat levelε∈(0,1] is deﬁned as
πX(ε) = inf/braceleftbig
d/greaterorequalslant1 : ESε(X)/lessorequalslantVaRε/d(X)/bracerightbig
, ε∈(0,1].
The existence and uniqueness of πX(ε) can be shown in the same way as the existence and
uniqueness of the PELVE. There are advantages and disadvantag es of working with both notions; see
Li and Wang (2022, Remark 2). In our context, the main advantage of using the dual PELVE is that
πX(ε) is ﬁnite for all ε∈(0,1], while Π X(ε) is ﬁnite only when E[X]/lessorequalslantVaRε(X).
Note that for Xwith a discontinuous quantile function, there may not exist dsuch that ES ε(X) =
VaRε/d(X). In order to guarantee the above equivalence, we make the follow ing assumption for the
quantile function, represented by general function f.
Assumption 1. The function fis strictly decreasing and continuous, and/integraltext1
0|f(s)|ds <∞.
LetXbe the set of X∈L1with quantile function satisfying Assumption 1. The requirement that
the quantile function of Xis continuous and strictly decreasing is equivalent to that the distrib ution
function is continuous and strictly increasing in (ess-inf( X),ess-sup(X)); seeEmbrechts and Hofert
(2013). We limit our discussion to random variables X∈ X, which include the most common models
in risk management.
Proposition 2. ForXwith quantile function satisfying Assumption 1andε∈(0,1), we have
ΠX(ε/πX(ε)) =πX(ε)andπX(ΠX(ε)ε) = Π X(ε)ifE[X]/lessorequalslantVaRε(X). Furthermore, πX(ε)is the
unique solution d/greaterorequalslant1to the equation
ESε(X) = VaR ε/d(X).
It is straightforward to verify Proposition 2. By Proposition 2, we can calibrate the distribution
functions from dual PELVE instead of PELVE, and the calibrated dis tributions should satisfy the
equation ES ε(X) = VaR ε/d(X).
4.2 An integral equation associated with dual PELVE
In order to calibrate distributions from the dual PELVE, we can equ ivalently focus on quantile
functions. Let us consider X∈ Xandf(s) = VaR s(X). Then, solving πX(ε) is the same as solving z
14in following equation:/integraldisplayy
0f(s)ds=yf(zy) (3)
fory=ε. The solution is z= 1/πX(y). Asf(s) = VaR s(X),fsatisﬁes Assumption 1. Denote by C
the set of all fsatisfying Assumption 1. For any f∈ C, the existence of the solution zis guaranteed by
the mean-value theorem and its uniqueness is obvious. For y∈(0,1], letzf(y) be the solution to ( 3)
associated with f. Clearly, zf(y)/lessorequalslant1 andy/ma√sto→yzf(y) is strictly increasing. This is similar to Lemma
1for the two-point case. Obviously, zf(y) is also location-scale invariant under linear transformation
onf∈ C. That is, zλf+b=zfforλ >0 andb∈R. Furthermore, zfis continuous as fis continuous
and strictly decreasing. The next proposition is a simple connection b etweenzfandπX.
Proposition 3. For any fsatisfying Assumption 1,X=f(U)for some U∼U(0,1)has the dual
PELVEπX(y) = 1/zf(y)for ally∈(0,1)wherezfis solution to (3). ForXwith quantile function
satisfying Assumption 1, there exists fsatisfying Assumption 1such that X=f(U)for some U∼
U(0,1)and the solution to (3)iszf(y) = 1/πX(y)for ally∈(0,1).
Proof.For any fsatisfying Assumption 1, letF(x) = 1−f−1(x). Hence, Fis a continuous and
strictly increasing distribution function and F−1(s) =f(1−s) fors∈(0,1). LetU∼U(0,1) and
X=F−1(U) =f(1−U). ThenX∈ XandX∼F. AsF−1(1−s) =f(s), we have πX(y) = 1/zf(y).
TakeU′= 1−U. We have X=f(U′) andU′∼U(0,1).
ForX∈ X, letf(s) = VaR s(X). Then, we have zf(y) = 1/πX(y) fory∈(0,1]. Furthermore, we
haveF−1(s) =f(1−s). Therefore, there exists U∼U(0,1) such that X=f(1−U). LetU′= 1−U.
Then, we have X=f(U′) andU′∼U(0,1).
Proposition 3allows us to study zinstead of πfor the calibration problem. The integral equation
(3) can be very helpful in characterizing the distribution from the dua l PELVE.
Some examples of πXandzfare listed in Table 2, which is corresponding to the PELVE presented
in Table 1.
Table 2: Example of πXandzf
X πX(ε) f zf
U(0,1) πX(ε) = 2 f(x) = 1−x zf(y) = 1/2
Exp(λ) πX(ε) =e f(x) =−log(x)/λ zf(y) = 1/e
GPD(ξ)πX(ε) = (1−ξ)−1
ξf(x) =/braceleftBigg
1/ξ/parenleftbig
x−ξ−1/parenrightbig
ξ/ne}ationslash= 0
−log(x)ξ= 0zf= (1−ξ)1
ξ
For a given dual PELVE curve π, we ﬁnd the solution to the integral equation by the following
steps.
151. Letz(y) =1
π(y)for ally∈(0,1].
2. Findf∈ Cthat satisﬁes/integraltexty
0f(s)ds=yf(z(y)y) for ally∈(0,1].
3. By Proposition 3,X=f(U) for some U∼U(0,1) will have the given dual PELVE π.
Therefore, we will focus on characterizing ffrom a given z: (0,1]→(0,1] below. Generally, it is
hard to characterize fexplicitly. We ﬁrst formulate the problem as an advanced diﬀerential equation,
which helps us to ﬁnd solutions.
4.3 Advanced diﬀerential equations
In this section, we show that the main objective ( 3) can be represented by a diﬀerential equation.
The use of diﬀerential equations in computing risk measures has not been actively developed. The only
paper we know is Balb´ as et al. (2017) which addresses a diﬀerent problem.
Let us recall the integral equation ( 3) from Section 4.2. For a function f∈ C, we solve the function
zf: (0,1)→Rfrom (3). We represent ( 3) by an advanced diﬀerential equation using the following
steps.
1. Letωf(y) =yzf(y). It is easy to see that zf(y)/lessorequalslant1. Hence, ωfis strictly increasing and
continuous on (0 ,1] andωf(y)/lessorequalslanty.
2. Letufbe the inverse function of ωf. We have that uf: (0,zf(1)]/ma√sto→(0,1] is a continuous and
strictly increasing function and uf(w)/greaterorequalslantw.
3. Replacing ywithuf(w) in (3), we have f(w) =/integraltextuf(w)
0f(w)ds/uf(w).
4. Assume ufis continuously diﬀerentiable. It is clear that fis continuously diﬀerentiable on
(0,zf(1)). Hence, we can represent ( 3) by the following advanced diﬀerential equation
f′(w)+u′
f(w)
uf(w)(f(w)−f(uf(w))) = 0.
For a given function z: (0,1]→R, letu=ω−1such that ω(y) =yz(y) fory∈(0,1]. Then, we
solve the function fby the following diﬀerential equation
f′(w)+u′(w)
u(w)f(w)−u′(w)
u(w)f(u(w)) = 0. (4)
Ifz= 1/πXfor some X∈ X, thenuis a strictly increasing and continuous function such that
u(w)/greaterorequalslantw. Furthermore, if zis continuously diﬀerentiable, then we can characterize all X∈ Xwith
πX= 1/zby (4). Asu′(w)/u(w)/greaterorequalslant0 andu(w)/greaterorequalslantw, (4) is a linear advanced diﬀerential equation
16which is well studied in the literature. In Berezansky and Braverman (2011), it is shown that there
exists a non-oscillatory solution for ( 4).
4.4 The constant PELVE curve
We ﬁrst solve the case that z(y) =cfor ally∈(0,1] and some constant c∈(0,1). As we can
see from Table 2, the power function and logarithm function have constant zf. Iff(x) =λxα+bfor
α >−1, we can see that ( α+1)−1/α=c. In this section, we can characterize all the other solutions
which can not be expressed as a linear transformation of the power function. That is, we will see that
the set
{f∈ C:zf(y) =z(y), y∈(0,1]}
is not a location-scale class. Hence, we can answer the question at t he beginning of the section; that
is, in the case the PELVE is a constant, the set {X∈ X: ΠX=c}is not a location-scale class.
Theorem 2. Forc∈(0,1), anyXwith quantile function satisfying Assumption 1andπX(ε) = 1/c
forε∈(0,1)can be written as X=f(U)for some U∼U(0,1)andfsatisfying Assumption 1.
Furthermore, such fhas the form
f(y) =C1+C2yα+O/parenleftbig
yζ/parenrightbig
,
whereαis the root of (α+1)−1/α=c,ζ >max{0,α},C1,C2∈R,C2α <0andO(yζ)is a function
such that limsupy→0O(yζ)/yζis a constant.
The proof of Theorem 2is provided in Appendix B. As we can see, Theorem 2characterizes all
X∈ Xsuch that πX(ε) = 1/c. Ifc∈(0,1/e),αis negative. As ζ >0, we can see that X=f(U)
is regularly varying of index α. Hence, one can then consider the Pareto distribution with surviva l
function S(x) =xαas a representative solution for the tail behavior. An open questio n is that, in the
general case that the PELVE is not necessarily constant, whethe r all the solutions behave similarly
regarding their tail behavior.
Another interesting implication of the theorem and its proof is that o ne can give a non-trivial
solution for zis a constant.
Example 3. Forc∈(0,1), let (θ,η) be a solution of


clogc=−ηexp(−η
tan(η))
sin(η),
θ=−η
tan(η).
17Then, the function f, given by
f(y) =C1+C2yα+C3yζsin(−σlog(y)),0< y <1, (5)
satisﬁes/integraltexty
0f(s)ds=yf(cy) and Assumption 1, whereαsolves (α+ 1)−1/α=c,ζ=θ/logc−1,
σ=−η/logc,C2is a constant such that C2α <0 and 0< C3<−C2α/(ζ+|σ|).
If we take C3= 0, we get the simplest power function for z(x) =c. IfC3/ne}ationslash= 0, the solution ( 5) is
not a linear transformation of the power function solution.
Let us look at the example where π(ε) = 2 for all ε∈(0,1], which means z(y) = 1/2 fory∈(0,1].
As we have seen in Table 2,f(y) = 1−ycan be a solution that leads to X∼U(0,1). Furthermore,
according to Example 3, we can have another solution
f(y) = 1−yα+Cyζsin(−σlog(y)),
whereα= 1,C= 0.05096,ζ= 4.0184 and σ=−15.4090. In the left of Figure 7, we have depicted
the two solutions for f. We can see they are quite diﬀerent when ygoes to 1. In the right of Figure 7,
we numerically calculate zfforf(y) = 1−yα+Cyζsin(−σlog(y)). We can see its numerical value is
almost 1/2 and the discrepancy is due to limited computational accur acy.
Figure 7: Non-unique calibrated functions for z(y) = 1/2.
0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 100.10.20.30.40.50.60.70.80.91
0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 100.10.20.30.40.50.60.70.80.91
By letting X=f(U), we get πX(ε) = 2 for all ε∈(0,1] and such Xdoes not follow the uniform
distribution.
4.5 A numerical method
In general, it is hard to get an explicit solution to ( 4). Here we present a numerical method to
solve (4). Let us introduce the following process.
181. Leta0= 1,a1=a, ...,an=u−1(an−1).
2. Fora∈(0,1), letξbe the solution to (1 −ξ)1
ξ=a. Let
f0(x) =

1
ξ/parenleftbig
x−ξ−1/parenrightbig
, ξ/ne}ationslash= 0,
−log(x), ξ= 0,(6)
on [a,1].
3. We can solve the following ODE on [ a2,a1]:
f′
1(w)+u′(w)
u(w)f1(w) =u′(w)
u(w)f0(u(w)), w∈[a2,a1].
4. Now we can repeat step 3 by induction on [ an+1,an] forn >1 by solving
f′
n(w)+u′(w)
u(w)fn(w) =u′(w)
u(w)fn−1(u(w)), w∈[an+1,an].
5. In general, the solution for diﬀerential equationdy
dx+P(x)y=Q(x) is
y=e−/integraltextxP(λ)dλ/bracketleftbigg/integraldisplayx
e/integraltextλP(ε)dεQ(λ)dλ+C/bracketrightbigg
.
So, we get the following solution for fn:
fn(w) =e/integraltextan
wu′(λ)
u(λ)dλ/bracketleftbigg
fn−1(an)−/integraldisplayan
we−/integraltextan
λu′(ε)
u(ε)dεu′(λ)
u(λ)fn−1(u(λ))dλ/bracketrightbigg
, w∈[an+1,an].
6. Finally, let f=fnon [an+1,an].
Note that since we start with a strictly decreasing function, then f rom equation ( 4) we have
f′(w) =u′(w)
u(w)(f(u(w))−f(w))<0,
sofremains strictly decreasing.
The solution produced by the numerical method heavily relies on f0. The equation ( 4) does
not have a unique solution, but the solution from the above process is unique. We set f0as (6) by
assuming zcan be extended from (0 ,1] toR+and setz(y) =afor ally >1. We use this assumption
for simpliﬁcation as we can know that ( 6) satisﬁes ( 4) for a constant zfrom Section 4.4. This choice of
f0is the same as the choice of k(ε) in the two-point calibration problem, and this reﬂects our subject ive
view of the importance of the Pareto distribution in risk management . Especially, when z(y) =cfor
19some constant c, we have u(x) =x/c. Therefore, ( 5) gives
fn(w) =an
w/bracketleftbigg
fn−1(an)−/integraldisplayan
w1
anfn−1/parenleftbiggλ
c/parenrightbigg
dλ/bracketrightbigg
.
If we set f0as (6), we can have f1also in the form of ( 6). Then, it is obvious that fnis also in the
form of ( 6). Therefore, the numerical method gives the simplest power func tion or logarithm function
whenz(y) is a constant on (0 ,1] as Table 2, which leads to the generalized Pareto distribution for X.
4.6 Numerical calibrated quantile function
Now let us explore the method in Section 4.5with simulation. Here we present the results for a
few cases. In Figures 8to11, we compare the solution from the numerical method with the stand ard
formula in Table 2in the left panel, and compare/integraltexty
0f(s)dswithyf(z(y)y) to validate the equation
(3) in the right panel.
We ﬁrst try some examples where zis constant as shown in Table 2, i.e.z(x) = 1/2 (Figure 8),
z(x) = 1/e(Figure9) andz(x) = 0.910(Figure10). For Figure 8to10, we can see that the numerical
method provides exactly the same function fas Table 2.
In Figure 11, we check the case z(x) = log( x/(1−e−x))/x. The function f(x) =e−xsatisﬁes
(3). We can see that the solution from the numerical method is close to a function of the form
f(x) =λe−x+b, which is known to satisfy the integral equation.
Figure 8: Calibrated function and validation for z(x) = 1/2
0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 100.10.20.30.40.50.60.70.80.91
0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 100.050.10.150.20.250.30.350.40.450.5
5 Technical properties of the PELVE
We now take a turn to study several additional properties of PELV E. In particular, we will obtain
results on the monotonicity and convergence of the dual PELVE as well as the PELVE.
20Figure 9: Calibrated function and validation for z(x) = 1/e
0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1024681012
0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 100.10.20.30.40.50.60.70.80.91
Figure 10: Calibrated function and validation for z(x) = 0.910
0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 10510152025
0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 100.20.40.60.811.2
5.1 Basic properties of dual PELVE
The following proposition that shows the PELVE and dual PELVE shar e some basic properties
such as monotonicity (i), location-scale invariance (ii) and shape rele vance (iii)-(iv) below.
Proposition 4. Suppose the quantile function of Xsatisﬁes Assumption 1andε∈(0,1].
(i)ΠX(ε)is increasing (decreasing) in εif and only if so is πX(ε).
(ii) For all λ >0anda∈R,πλX+a(ε) =πX(ε).
(iii)πf(X)(ε)/lessorequalslantπX(ε)for all strictly increasing concave functions: f:R→Rwithf(X)∈ X.
(iv)πg(X)(ε)/greaterorequalslantπX(ε)for all strictly increasing convex functions: g:R→Rwithg(X)∈ X.
The statements (ii)-(iv) areparallel to the correspondingstatem ents in Theorem 1 of Li and Wang
(2022) on PELVE. The proof of Proposition 4is put in Appendix C. Proposition 4allows us to study
21Figure 11: Calibrated function and validation for z(x) = log(x/(1−e−x))/x
0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 100.511.5
0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 100.10.20.30.40.50.60.7
the monotonicity and convergence of the PELVE by analyzing the co rresponding properties of the
dual PELVE, which is more convenient in many cases. In the following s ections, we focus on ﬁnding
the conditions which make the dual PELVE monotone and convergen t at 0. By Proposition 4, those
conditions can also apply to the PELVE.
5.2 Non-monotone and non-convergent examples
In this section, we study the monotonicity and convergence of dua l PELVE. For monotonicity, we
have shown some well-known distributions such as normal distributio n, t-distribution and lognormal
distribution have monotone PELVE curves in Example 3. However, the PELVE is not monotone for
allX∈ X. Below we provide an example.
Example 4 (Non-monotone PELVE) .Let us consider the following density function gon [−2,2],
g(x) =1
2/parenleftbig
(x+2)1{x∈[−2,−1]}−x1{x∈(−1,0]}+x1{x∈(0,1]}+(2−x)1{x∈(1,2]}/parenrightbig
.
ForXwith density function g, Figure 12presents the value of Π X(ε) forε∈(0,0.5). As one can see,
the PELVE is not necessarily decreasing, and so is the dual PELVE.
Fortheconvergence,itisclearthat πX(ε)iscontinuousin(0 ,1)forX∈ X. Therefore,lim ε→pπX(ε)
exists for all p∈(0,1). However, both Π X(ε) andπX(ε) are not well deﬁned at ε= 0. If lim ε→0πX(ε)
exists, we can deﬁne πX(0) as the limit, and Π X(0) similarly. However, the following example shows
that the limit does not exist for some X∈ X.
Example 5 (No limit at 0) .We can construct a random variable X∈ Xsuch that lim ε→0πX(ε) does
not exist from the integral equation ( 3) in Section 4.2. Equivalently, we will ﬁnd a continuous and
strictly decreasing function f∈ Csuch that lim y→0zf(y) does not exist. Let cbe the Cantor ternary
22Figure 12: PELVE for Xwith density g
0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.51.61.71.81.922.12.22.3PELVE
function on [0 ,1]. Note that x/ma√sto→c(x) is continuous and increasing on (0 ,1) andc(x/3) =c(x)/2. Let
f(x) =−c(x)−xlog2/log3. It is clear that f∈ Candf(x/3) =f(x)/2. For each y∈(0,1], we have
yf(zf(y)y) =/integraldisplayy
0f(x)dx
= 2/integraldisplayy
0f/parenleftbigg1
3x/parenrightbigg
dx= 6/integraldisplay1
3y
0f(x)dx= 2yf/parenleftbigg1
3yzf/parenleftbigg1
3y/parenrightbigg/parenrightbigg
=yf/parenleftbigg
yzf/parenleftbigg1
3y/parenrightbigg/parenrightbigg
.
Sincefis strictly decreasing, zf(y) =zf(y/3) fory∈(0,1]. It means that zf(y) is a constant
on (0,1] if lim y→0zf(y) exists. Now, let us look at two particular points of zf(y). We can show that
zf(1)/ne}ationslash=zf(4/9). Letz= (log2/log3+1)−(log3/log2). Then, we have 1 /3< z≈0.46<1/2. Fory= 1,
we have/integraltext1
0c(s)ds=c(z) = 1/2 and/integraltextc
0slog2/log3ds=zlog2/log3. Therefore, we get zf(1) =z <1/2.
Fory= 4/9, we have
f/parenleftbigg4
9zf/parenleftbigg4
9/parenrightbigg/parenrightbigg
=9
4/integraldisplay4/9
0f(s)ds
=−9
4/parenleftBigg
1
log2
log3+1/parenleftbigg4
9/parenrightbigglog 2
log 3+1
+1
12+1
2/parenleftbigg4
9−1
3/parenrightbigg/parenrightBigg
<−0.68< f/parenleftbigg2
9/parenrightbigg
≈ −0.64.
Asfis strictly decreasing, we have (4 /9)zf(4/9)>2/9 which implies zf(4/9)>1/2> zf(1). As a
result, lim y→0zf(y) does not exist. Therefore, we have a continuous and strictly dec reasingfsuch
that lim y→0zf(y) does not exist.
235.3 Suﬃcient condition for monotonicity and convergence
In risk management applications, for a random variable Xmodeling a random loss, the behavior
of its tail is the most important. Let F[p,1]be the upper p-tail distribution of F(see e.g., Liu and Wang
(2021)), namely
F[p,1](x) =(F(x)−p)+
1−p, x∈R.
We will see that the dual PELVE of F[p,1]is a part of the dual PELVE of F.
Lemma 2. LetFbe the distribution function of Xwith quantile function satisfying Assumption 1.
Forp∈(0,1)andX′∼F[p,1], it holds
πX′(ε) =πX(ε(1−p)).
Proof.It is clear that VaR ε(X′) = VaR ε(1−p)(X) and ES ε(X′) = ES ε(1−p)(X). Therefore,
πX′(ε) = inf{d/greaterorequalslant1 : ESε(X′)/lessorequalslantVaRε/d(X′)}
= inf{d/greaterorequalslant1 : ESε(1−p)(X′)/lessorequalslantVaRε(1−p)/d(X′)}=πX(ε(1−p)).
Thus, we have the desired result.
The tail distribution can provide a condition to check whether the du al PELVE is decreasing.
Proposition 5. LetFbe the distribution function of Xwith quantile function satisfying Assumption
1. Ifx/ma√sto→F−1/parenleftbig
(1−p)F(x)+p/parenrightbig
is convex (concave) for all p∈(0,1), thenπXandΠXare decreasing
(increasing).
Proof.For anyp∈(0,1), letX′∼F[p,1]. By Lemma 2, we have πX′(ε) =πX(ε(1−p)). Furthermore,
we have
/parenleftBig
F[p,1]/parenrightBig−1
(t) =F−1((1−p)t+p) =F−1/parenleftBig
(1−p)F/parenleftbig
F−1(t)/parenrightbig
+p/parenrightBig
, t∈[0,1].
LetU∼U(0,1),X=F−1(U) andX′= (F[p,1])−1(U).
We assume that x/ma√sto→F−1/parenleftbig
(1−p)F(x)+p/parenrightbig
is a convex function on (ess-inf( X),ess-sup(X)) ﬁrst.
Letf:R→Rbe a strictly increasing convex function such that f(x) =F−1((1−p)F(x) +p) for
x∈(ess-inf(X),ess-sup(X)).Then, we have X′=f(X). By Proposition 4, we getπX′(ε)/greaterorequalslantπX(ε). As
πX′(ε) =πX(ε(1−p)), we have πX(ε(1−p))/greaterorequalslantπX(ε) for allp∈(0,1). Thus, πXis decreasing. By
Proposition 4, we have Π Xis also decreasing.
On the other hand, if x/ma√sto→F−1/parenleftbig
(1−p)F(x)+p/parenrightbig
is concave, we have πX(ε(1−p))/lessorequalslantπX(ε) for all
p∈(0,1) andπXis increasing. So is Π X.
24The condition x/ma√sto→F−1/parenleftbig
(1−p)F(x)+p/parenrightbig
is convex (concave) for all p∈(0,1) is generally hard to
check. Intuitively, this condition means that F[p,1]has a less heavy tail compared to F. We can further
simplify this condition by using the hazard rate function. For X∈ Xwith distribution function Fand
density function f, letS= 1−Fbe the survival function and η=f/Sbe the hazard rate function.
AsFis continuous and strictly increasing, Sis continuous and strictly decreasing.
Theorem 3. ForXwith quantile function satisfying Assumption 1, letηbe the hazard rate function
ofX. If1/ηis second-order diﬀerentiable and convex (concave), then πXandΠXare decreasing
(increasing).
The proof of Theorem 3is provided in Appendix C.
Example 6. For the normal distribution, we can give a short proof of the conve xity of 1 /η. LetS
be the survival function of the standard normal distribution and fits density. Let I(x) = 1/η(x) =
S(x)/f(x) = exp/parenleftbig
x2/2/parenrightbig/integraltext−x
−∞exp/parenleftbig
−s2/2/parenrightbig
ds. One can easily see that
I′(x) =xI(x)−1 (7)
which gives I′′(x) =xI′(x)+I(x). This with ( 7) implies that
I′′(x) =/parenleftbig
1+x2/parenrightbig
I(x)−x. (8)
First, consider the negative line i.e., x <0. In this case ( 7) and (8) implyI′(x) =xI(x)−1<0,
andI′′(x) = (1+ x2)I(x) +(−x)>0.The implication of the two relations is that Iis a convex and
decreasing function on negative line. Now we consider the case x >0. In this case, let i(x) =I′(−x).
From what we have proved it is clear that iis an increasing function on x >0. On the other hand, we
haveI(x)+I(−x) = 1/f(x) =√
2πexp/parenleftbig
x2/2/parenrightbig
. This combined with ( 7) gives us
I′(x) =x(I(x)+I(−x))+i(x) =x√
2πexp/parenleftbig
x2/2/parenrightbig
+i(x),x >0.
This means I′is an increasing function on x >0 as it is a summation of two other increasing functions,
soIis convex on the positive line as well.
Figure13presents the curve 1 /ηfor the generalized Pareto distribution, the Normal distribution,
the t-distribution and the Lognormal distribution. For distribution s GPD(1 /2), N(0,1) and t(2), we
can see that the curves 1 /ηare convex, and this coincides with decreasing PELVE shown in Examp le2.
For the Lognormal distribution, the shape of 1 /ηdepends on σ. As shown in Example 2, the PELVE
for LN(σ) is visibly decreasing for σ2= 0.04 and increasing for σ= 1. Corresponding to the above
observations, we see that 1 /ηis convex for σ2= 0.04 and concave for σ2= 1.
25Figure 13: 1 /ηfor GPD(1 /2), N(0,1), t(2), LN(0 ,2) and LN(1) in blue curves; in the right panel, the
red curve is linear
0 200 400 600 800 10000100200300400500600GPD(1/2)
-5 0 502468105N(0,1)
-10 -5 0 5 10020040060080010001200t(2)
1 2 3 40.10.150.20.25LN(0.2)
10 11 12 13 14 15 16 17 18 19 203.544.555.566.5LN(1)
Hazard function
Linear function
Corollary 1. If the hazard rate of a random variable Xis second-order diﬀerentiable and concave,
thenπXandΠXare decreasing.
Proof.Just note that if ηis concave, then ηη′′is non-positive. It follows that
/parenleftbigg1
η/parenrightbigg′′
=/parenleftbigg
−η′
η2/parenrightbigg′
=2(η′)2−ηη′′
η3/greaterorequalslant0.
Thus, 1/ηis convex, and the desired statement follows from Theorem 3.
The corollary above is a result of the fact that the concavity of ηimplies convexity of 1 /η.
Therefore, concave ηalways leads to decreasing PELVE. For example, the Gamma distribut ion G(α,λ)
with density f(x) =λαtα−1e−λt/Γ(α) has concave hazard rate function when α >1. Furthermore, by
Theorem 3, we can easily ﬁnd more well-known distributions that have decreasin gπX.
As the tail distribution determines πXaround 0, we can focus on the tail distribution to discuss
the convergence of πXat 0. Note that if the survival distribution function is regularly vary ing, then its
tail parameter one-to-one corresponds to the limit of Π Xat 0 as shown by Theorem 3 of Li and Wang
(2022). Hence, the limit of Π X, if it exists, can be useful as a measure of tail heaviness, and it is we ll
deﬁned even for distributions that do not have a heavy tail. By the m onotone convergence theorem,
we have lim ε→0πX(ε) exists if πXis monotone. The limit may be ﬁnite or inﬁnite.
Corollary 2. ForXwith quantile function satisfying Assumption 1, letηbe the hazard rate of X. If
1/η(x)is second-order diﬀerentiable and convex (concave) in/parenleftbig
F−1(δ),ess-sup(X)/parenrightbig
for some δ∈(0,1),
thenlimε→0πX(ε)exists. In particular, this is true if ηis second-order diﬀerentiable and concave on
/parenleftbig
F−1(δ),ess-sup(X)/parenrightbig
.
Proof.LetX′∼F[δ,1]. Then, the survival function for X′isSX′(x) =S(x)/(1−p) forx/greaterorequalslantF−1(δ).
The density function is fX′(x) =f(x)/(1−p) forx/greaterorequalslantF−1(δ). Therefore, the hazard rate function is
ηX′(x) =f(x)/S(x) =η(x) forx/greaterorequalslantF−1(δ).
26As 1/η(x) is convex (concave) when x > F−1(δ), we have 1 /ηX′(x) is convex (concave). By
Theorem 3, we have πX′(ε) is decreasing (increasing) on (0 ,1). As a result, we have πX(ε) is decreasing
(increasing) on (0 ,δ) and lim ε→0πX(ε) exists.
By Corollary 1, ifηis concave on ( F−1(δ),ess-sup(X)), 1/ηis convex on ( F−1(δ),ess-sup(X))
and lim ε→0πX(ε) also exists.
Example 7. If limε→0πX(ε) is a constant, we have lim ε→0Πε(X) = lim ε→0πX(ε) asπX(ΠX(ε)ε) =
ΠX(ε). We give the numerical values of Π X(ε) at very small probability levels εfor normal, t, and log-
normal distributions. These distributions do not have a constant P ELVE curve, and using Corollary 2
we can check that their PELVE have limits. As we can see from Table 3, PELVE can still distinguish
the heaviness of the tail even when εis very small. The heavier tailed distributions report a higher
PELVE value. For the normal distribution and the log-normal distrib ution with σ= 0.2, the value of
PELVE is close to e≈2.7183 asε↓0. From the numerical values, it is unclear whether Π X(ε)→e
for all log-normal distributions, but there is no practical relevanc e to compute Π X(ε) forε <10−11in
applications.
Table 3: Values of Π X(ε)
Distribution N LN(1) LN(0 .5) LN(0 .2) t(2) t(3)
ε= 10−102.6884 2.9167 2.7944 2.7290 4.0000 3.3750
ε= 10−112.6909 2.9077 2.7920 2.7287 4.0000 3.3750
6 Applications to datasets used in insurance
In this section, we apply the PEVLE calibration techniques to datase ts used in insurance to show
how to use the calibrated distribution in estimating risk measure value s and simulation.
6.1 Dental expenditure data
In this example, we apply the calibration model to the 6494 complete h ousehold component’s
total dental expenditure data from Medical Expenditure Panel S urvey for 2020. An earlier version of
the same dataset is used by Behan et al. (2010) to study the relationship between worker absenteeism
and overweight or obesity. The main purpose of this experiment is to construct tractable models, with
continuousand simplequantilefunctions, which havesimilarriskmeasu revaluesasthe originaldataset,
and the same PELVE at certain levels. We present in Figure 14two quantile functions calibrated from
ΠX(ε1) and Π X(ε2), with ( ε1,ε2) = (0.01,0.05) and ( ε1,ε2) = (0.05,0.1), respectively. The two
calibrated quantile functions are scaled up according to the empirica l VaRε1(X) and VaR ε2(X). By
27Theorem 1, we can calibrate the quantile functions from Case 4 when ( ε1,ε2) = (0.01,0.05), and from
Case 5 when ( ε1,ε2) = (0.05,0.1). As mentioned before, for ( ε1,ε2) = (0.05,0.1), we set the calibrated
quantile function in (0 ,c1ε1) as the Pareto quantile function. Hence, there is no ﬂat part in the two
calibrated quantile functions shown in Figure 14. As we can see, both the two calibrated quantile
functions ﬁt the empirical quantile functions well. The calibrated qua ntile function can be regarded as
a special parameterized model for tail distribution, which can ﬁt th e value of VaR and ES at speciﬁed
levels. With the parameterized calibrated model, we can estimate the value of tail risk measures (see
Liu and Wang (2021)) such as ES, VaR, and Range-VaR (RVaR), amongst others. In T ables4and5,
we compute the values of ES and RVaR for the calibrated model and c ompare them with empirical ES
and RVaR values, respectively, where the risk measure RVaR is deﬁn ed as
RVaRα,β(X) =1
β−α/integraldisplayα
βVaRγ(X)dγ
for 0/lessorequalslantα < β < 1; seeCont et al. (2010) andEmbrechts et al. (2018). As we scale the calibrated quan-
tile function to empirical VaR ε1(X) and VaR ε2(X), the calibrated ES and empirical ES are identical at
levelsε1ΠX(ε1) andε2ΠX(ε2) by the deﬁnition of PELVE. For other probability levels, the calibrat ed
ES and RVaR in Tables 4and5are close to their empirical counterparts. When ( ε1,ε2) = (0.01,0.05),
it may only be useful to compute calibrated ES p(X) forp <0.05ΠX(0.05) = 0.11591 because the
calibrated quantile function is arbitrary beyond the level 0 .11591. If we need to estimate ES or RVaR
for a larger probability level, we can choose a higher ε2as long as E[X]/lessorequalslantVaRε2(X) is satisﬁed. For
this dataset, the highest ε2we can use is 0.1983.
Using the methods in Section 3, for quantile levels between (0 ,ε1), the distribution calibrated
from one point ( ε1,c1) is the same as the one calibrated from two points ( ε1,c1) and (ε2,c2). Hence,
the results for ES pof the one-point calibrated function are also shown in Tables 4and5in the cells
p/lessorequalslantε1.
Table 4: Empirical ES and calibrated ES for the dental expenditure d ata
p 0.01 0.05 0.1 0.2 0.3
Empirical ES p 10073.1 5361.7 3624.8 2317.9 1696.7
Calibrated ES pfrom (ε1,ε2) = (0.01,0.05) 11703.9 5357.7 3759.1 - -
Calibrated ES pfrom (ε1,ε2) = (0.05,0.1) 10878.1 5439.6 3711.3 2293.7 1696.4
6.2 Hospital costs data
In this example, we apply the calibration process to the Hospital Cos ts data of Frees(2009) which
were originally from the Nationwide Inpatient Sample of the Healthcar e Cost and Utilization Project
28Figure 14: Empirical and calibrated VaR εfor the dental expenditure data
0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4010002000300040005000600070008000900010000
Table 5: Empirical RVaR and calibrated RVaR for the dental expendit ure data
(α,β) (0 .01,0.02) (0.02,0.05) (0.05,0.1)
Empirical RVaR α,β 5748.5 3662.4 1887.9
Calibrated RVaR α,βfrom (ε1,ε2) = (0.01,0.05) 5003.7 3360.2 2160.6
Calibrated RVaR α,βfrom (ε1,ε2) = (0.05,0.1) 5634.6 3561.8 1983.1
(NIS-HCUP). The data contains 500 hospital costs observations with 244 males and 256 females which
can be regarded as the losses of the health insurance policies. Using the calibration model of the
two-point constraint problem, we calibrate quantile functions for f emales and males from PELVE at
probability levels ε1= 0.05 andε2= 0.1, which are shown in Figure 15. Except for estimating the
risk measure, the calibrated distribution is useful in simulation. Assu me the insurance company wants
to know the top 10% hospital costs; that is X|X >VaR0.1(X) whereXis the hospital costs. There
are only 24 available data for males and 25 available data for females, w hich would be not enough for
making statistically solid decisions. To generate more pseudo-data p oints, we can simulate data from
the calibrated distribution; that is, we simulate data from F[p,1]whereFis the calibrated distribution
in Figure 15. Taking p= 0.9, we have F[p,1](t) = VaR (1−p)(1−t)(X) with VaR t(X) from Figure 15. We
simulate 1000 data from the calibrated distributions based on PELVE atε1= 0.05 andε2= 0.1. In
Figure16, we present two QQ plots of simulated data against empirical data fo r females and males
respectively. As we can see, the simulated data has a similar distribut ion as the empirical data. Those
simulated pseudo-data points can be used for estimating risk measu res or making other decisions. For
example,thesimulatedhospitalcostcanbeusedtodesignhealthins urancecontrastsorsetthepremium
29in complex systems, where sometimes methods based on simulated da ta are more convenient to work
with than methods relying on distribution functions. This may be seen as an alternative, smoothed,
version of bootstrap; recall that the classic bootstrap sample ca n only take the values represented in
the dataset. Furthermore, we compare the simulated data of hos pital costs for females and males in
Figure17, which shows that the distribution of the hospital costs for female s has a heavier tail than
that for males.
0 0.02 0.04 0.06 0.08 0.1 0.12 0.14 0.16 0.18 0.20123456104
Figure 15: Empirical and calibrated VaR εfor the hospital costs data
0 0.5 1 1.5 2 2.5
Calibrated quantile1050.511.522.5Empirical quantile105 Female
(a) Hospital costs for female0.5 1 1.5 2 2.5 3 3.5 4 4.5
Calibrated quantile1040.511.522.533.544.555.5Empirical quantile104 Male
(b) Hospital costs for male
Figure 16: QQ plot: simulated data VS empirical data
300 0.5 1 1.5 2 2.5
Hospital costs for female105024681012141618Hospital cost for male104
Figure 17: QQ plot of simulated data of hospital costs: female VS male
7 Conclusion
In this paper, we oﬀer several contributions to the calibration pro blem and properties of the
PELVE. The calibration problem concerns, with some given values fro m a PELVE curve, how one can
build a distribution that has this PELVE. We solve a few settings of calib ration based on a one-point
constraint, a two-point constraint, or the entire curve constra int. In particular, the calibration for a
given PELVE curve involves solving an integral equation/integraltexty
0f(s)ds=yf(z(y)y) for a given function
z, and this requires some advanced analysis and a numerical method in diﬀerential equations. For
the case that zis a constant curve, we can identify all solutions, which are surprisin gly complicated.
In addition, we see that if πXis a constant larger than e, which is observed from typical values in
ﬁnancial return data ( Li and Wang (2022)),Xshare the same tail behavior with the corresponding
Pareto solution. We also applied our calibration techniques to two dat asets used in insurance.
On the technical side, we study whether the PELVE is monotone and whether it converges at 0.
We show that the monotonicity of the PELVE is associated with the sh ape of the hazard rate. If the
inverse of the hazard rate is convex (concave), the PELVE is decr easing(increasing). The monotonicity
at the tail part of the PELVE leads to conditions to check the conve rgence of the PELVE at 0. If the
inverse of the hazard rate is convex (concave) at the tail of the d istribution, the limit of the PELVE
at 0 exists.
There are several open questions related to PELVE that we still do not fully understand. One
particular such question is whether the tail behavior, e.g., tail index , of a distribution is completely
determined by its PELVE. We have seen that this holds true in the cas e of a constant PELVE (see
31Theorem 2), but wedonothaveageneralconclusion. In the caseofregularly varyingsurvivalfunctions,
Li and Wang (2022, Theorem 3) showed that the limit of PELVE determines its tail param eter, but
it is unclear whether this can be generalized to other distributions. A nother challenging task is, for
a speciﬁed curve πon [0,1], to determine whether there exists a model XwithπX=π. The case
ofn-point constraints for large nmay require a new design of veriﬁcation algorithms. This question
concerns the compatibility of given information with statistical mode ls, which has been studied, in
other applications of risk management, by Embrechts et al. (2002,2016) andKrause et al. (2018).
Acknowledgements
The authors thank Xiyue Han for many helpful comments. Ruodu Wa ng is supported by the
Natural Sciences and Engineering Research Council of Canada (RG PIN-2018-03823, RGPAS-2018-
522590).
References
Acerbi, C. and Sz´ ekely, B. (2014). Backtesting expected short fall.Risk,27(11), 76-81.
Artzner, P., Delbaen, F., Eber, J.-M. and Heath, D. (1999). Coher ent measures of risk. Mathematical
Finance,9(3), 203–228.
Balb´ as, A., Balb´ as, B.andBalb´ as, R.(2017).Diﬀerentialequat ionsconnectingVaR andCVaR. Journal
of Computational and Applied Mathematics ,326, 247–267.
Barczy, M., Ned´ enyi, F. K. and S¨ ut˝ o, L. (2022). Probability equ ivalent level of Value at Risk and
higher-order Expected Shortfalls. Insurance: Mathematics and Economics ,108, 107–128.
BCBS (2019). Minimum Capital Requirements for Market Risk. February 201 9.Basel Committee on
Banking Supervision. Basel: Bank for International Settlements. BIS online publication No. bcbs457.
Behan, D. F., Cox, S. H., Lin, Y., Pai, J., Pedersen, H. W. and Yi, M. (20 10). Obesity and its relation
to mortality and morbidity costs. Society of Actuaries , 59.
Bellman, R. and Cooke, K. L. (1963). Diﬀerential-diﬀerence Equations . Academic Press, New York.
Berezansky, L. and Braverman, E. (2011). On nonoscillation of ad vanced diﬀerential equations with
several terms. Abstract and Applied Analysis ,2011, 637142.
Chambers, C. P. (2009). An axiomatization of quantiles on the doma in of distribution functions. Math-
ematical Finance ,19(2), 335–342.
Cont, R., Deguest, R. andScandolo, G. (2010).Robustness ands ensitivity analysisofriskmeasurement
procedures. Quantitative Finance ,10(6), 593–606.
32Embrechts, P. and Hofert, M. (2013). A note on generalized inver ses.Mathematical Methods of Opera-
tions Research ,77(3), 423–432.
Embrechts, P., Hofert, M. and Wang, R. (2016). Bernoulli and tail- dependence compatibility. Annals
of Applied Probability ,26(3), 1636–1658.
Embrechts, P., Liu, H. and Wang, R. (2018). Quantile-based risk sh aring.Operations Research ,66(4),
936–949.
Embrechts, P., McNeil, A. and Straumann, D. (2002).Correlationa nd dependence in risk management:
properties and pitfalls. Risk Management: Value at Risk and Beyond ,1, 176–223.
Embrechts, P., Puccetti, G., Ruschendorf, L., Wang, R. and Belera j, A. (2014). An academic response
to Basel 3.5. Risks,2(1), 25–48.
Emmer, S., Kratz, M. and Tasche, D. (2015). What is the best risk m easure in practice? A comparison
of standard measures. Journal of Risk ,18(2), 31–60.
Fiori, A. M. and Rosazza Gianin, E. (2023). Generalized PELVE and ap plications to risk measures.
European Actuarial Journal ,13(1), 307-339.
Frees, E. W. (2009). Regression Modeling with Actuarial and Financial Applicat ions. Cambridge
University Press. Cambridge.
Gneiting, T. (2011). Making and evaluating point forecasts. Journal of the American Statistical Asso-
ciation,106(494), 746–762.
Krause, D., Scherer, M., Schwinn, J. and Werner, R. (2018). Memb ership testing for Bernoulli and
tail-dependence matrices. Journal of Multivariate Analysis ,168, 240–260.
Kou, S. and Peng, X. (2016). On the measurement of economic tail risk.Operations Research ,64(5),
1056–1072.
Li, H. and Wang, R. (2022). PELVE: Probability equivalent level of Va R and ES. Journal of Econo-
metrics,234(1), 353–370.
Liu, F. and Wang, R. (2021). A theory for measures of tail risk. Mathematics of Operations Research ,
46(3), 1109–1128.
McNeil, A.J., Frey,R.andEmbrechts,P.(2015). Quantitative Risk Management: Concepts, Techniques
and Tools . Revised Edition. Princeton, NJ: Princeton University Press.
Rudin, W. (1987). Real and Complex Analysis . International Series in Pure and Applied Mathematics
(3rd Ed.). McGraw–Hill. New York.
Siewert, C. E. and Burniston, E. E. (1973). Exact analytical solut ions ofzez=a.Journal of Mathe-
matical Analysis and Applications ,43(3), 626–632.
Wang, R. and Zitikis, R. (2021). An axiomatic foundation for the Exp ected Shortfall. Management
Science,67, 1413–1429.
33A Omitted proofs in Section 3
Proof of Lemma 1.AsE[X]/lessorequalslantVaRε2(X)andε1< ε2,E[X]/lessorequalslantVaRε2(X)/lessorequalslantVaRε1(X). ByProposition
1 inLi and Wang (2022), ΠX(ε1)<∞and Π X(ε2)<∞.
For anyε∈(0,1) satisfying E[X]/lessorequalslantVaRε(X),
εΠX(ε) =εinf{c∈[1,1/ε] : EScε(X)/lessorequalslantVaRε(X)}
= inf{εc∈[ε,1] : ES cε(X)/lessorequalslantVaRε(X)}
= inf{k∈[ε,1] : ES k(X)/lessorequalslantVaRε(X)}.
LetA(ε) ={k∈[ε,1] : ES k(X)/lessorequalslantVaRε(X)}. For any k∈A(ε2), we have 1 /greaterorequalslantk/greaterorequalslantε2> ε1and
ESk(X)/lessorequalslantVaRε2(X)/lessorequalslantVaRε1(X). Hence, k∈A(ε1) and this gives A(ε2)⊆A(ε1). Therefore,
ε2ΠX(ε2) = infA(ε2)/greaterorequalslantinfA(ε1) =ε1ΠX(ε1).
Proof of Theorem 1.We will check the equivalent condition ( 2) between VaR and ES. Note that if
t/ma√sto→VaRt(X) is a constant on (0 ,ε), then Π X(ε) = 1. If t/ma√sto→VaRt(X) is not a constant on (0 ,ε), then
ΠX(ε) is the unique solution that satisﬁes ES εΠX(ε)(X) = VaR ε(X).
(i) Case 1 ,c2= 1. It is clear that VaR t(X) is a constant for t∈(0,c2ε2] and (2) is satisﬁed. Hence,
ΠX(ε2) = 1.Moreover, VaR t(X) is also a constant for t∈(0,c1ε1], which implies Π X(ε1) = 1.
(ii) Case 2 ,c1= 1 and 1 < c2/lessorequalslant1/ε2. Fort∈(0,ε1), VaR t(X) =Gz(t) is a constant for t∈(0,c1ε1).
Hence, Π X(ε1) = 1. Next, we check whether ES c2ε2(X) = VaR ε2(X). The value of ES c2ε2(X) is
ESc2ε2(X)
=1
c2ε2/parenleftbigg/integraldisplayε1
0ˆkdε+/integraldisplayε2
ε1(a1ε+b1)dε+/integraldisplayc2ε2
ε2(a2ε+b2)dε/parenrightbigg
=1
c2ε2/parenleftbigg
ε1ˆk+1
2a1(ε2
2−ε2
1)+b1(ε2−ε1)+1
2a2(c2
2ε2
2−ε2
2)+b2(c2ε2−ε2)/parenrightbigg
=1
c2ε2/parenleftbigg1
2a1(ε2−ε1)2+ˆkε2+1
2a2(c2ε2−ε2)2+˜k(c2ε2−ε2)/parenrightbigg
=1
c2ε2/parenleftbigg1
2(˜k−ˆk)(ε2−ε1)+ˆkε2+1
2(˜k−ˆk)(ε1+ε2)+˜k(c2ε2−ε2)/parenrightbigg
=˜k
The value of VaR ε2(X) isa2ε2+b2=˜k. Thus, ( 2) is satisﬁed. As VaR t(X) is not a constant for
t∈(0,c2ε2), we have Π X(ε2) =c2.
(iii) Case 3 , 1< c1/lessorequalslant1/ε1andc2=c1ε1
ε2. In this case, we have
VaRε1(X) =Gz(ε1) =k(ε1) =aε2+b=Gz(ε2) = VaR ε2(X)
34and ES c1ε1(X) = ES c2ε2(X) asc1ε1=c2ε2. Thus, we only need to check whether ES c2ε2(X) =
VaRε2(X). The value of ES c2ε2(X) is
ESc2ε2(X) =1
c2ε2/parenleftbigg/integraldisplayε1
0k(ε)dε+/integraldisplayε2
ε1k(ε1)dε+/integraldisplayc2ε2
ε2aε+bdε/parenrightbigg
=1
c2ε2/parenleftbigg
k+k(ε1)(ε2−ε1)+1
2a(c2
2ε2
2−ε2
2)+(k(ε1)−aε2)(c2ε2−ε2)/parenrightbigg
=1
c2ε2/parenleftbigg
k+k(ε1)(c2ε2−ε1)+1
2a(c2ε2−ε2)2/parenrightbigg
=1
c2ε2(k+k(ε1)(c2ε2−ε1)+k(ε1)ε1−k) =k(ε1).
The value of VaR ε2(X) is also k(ε1). Hence, ( 2) is satisﬁed and Π X(ε1) =c1, ΠX(ε2) =c2
becauset/ma√sto→VaRt(X) is not a constant on (0 ,ε1).
(iv) Case 4 , 1< c1/lessorequalslantε2/ε1and 1< c2/lessorequalslant1/ε2. The ﬁrst equivalent condition of ( 2) for VaR ε1(X) and
ESc1ε1(X) is satisﬁed because VaR t(X) =k(t) is the quantile function for GPD( ξ) with PELVE
c1andt∈(0,c1ε1). Hence, we have Π X(ε1) =c1. Moreover, ES c1ε1(X) = VaR ε1(X) =k(ε1).
We choose a1=k′(c1ε1) andb1such that a1c1ε1+b1=k(c1ε1). For the equivalent condition
between ES c2ε2(X) and VaR ε2(X), we can verify
ESc2ε2(X) =1
c2ε2/parenleftbigg/integraldisplayc1ε1
0k(ε)dε+/integraldisplayε2
c1ε1a1ε+b1dε+/integraldisplayc2ε2
ε2(a2ε+b2)dε/parenrightbigg
=1
c2ε2/parenleftbigg
c1ε1k(ε1)+1
2a1(ε2
2−c2
1ε2
1)+b1(ε2−c1ε1)+1
2a2/parenleftbig
c2
2ε2
2−ε2
2/parenrightbig
+b2(c2ε2−ε2)/parenrightbigg
=1
c2ε2/parenleftbigg
c1ε1k(ε1)+1
2a1(2c2ε2
2−ε2
2−c2
1ε2
1)+b1(c2ε2−c1ε1)+1
2a2(c2ε2−ε2)2/parenrightbigg
=1
c2ε2/parenleftbig
a1c2ε2
2+b1c2ε2/parenrightbig
=a1ε2+b1= VaR ε2(X).
Thus, (2) is satisﬁed and we have Π X(ε2) =c2.
(v) Case 5 ,ε2/ε1< c1/lessorequalslant1/ε1andc1ε1
ε2< c2/lessorequalslant1/ε2. The equality between VaR ε1(X) and ES c1ε1(X)
can be checked by
ESc1ε1(X) =1
c1ε1/parenleftbigg/integraldisplayε1
0k(ε)dε+/integraldisplayε2
ε1(a1ε+b1)dε+(a1ε2+b1)(c1ε1−ε2)/parenrightbigg
=1
c1ε1/parenleftbigg
k+1
2a1(ε2
2−ε2
1)+(k(ε1)−a1ε1)(ε2−ε1)+(a1ε2+b1)(c1ε1−ε2)/parenrightbigg
=1
c1ε1(k+a1(ε2−ε1)(c1ε1−1/2(ε2+ε1))+k(ε1)(c1ε1−ε1))
=1
c1ε1(k+k(ε1)ε1−k+k(ε1)(c1ε1−ε1)) =k(ε1) =Gz(ε1) = VaR ε1(X).
35The equality between VaR ε2(X) and ES c2ε2(X) can be checked by
ESc2ε2(X) =1
c2ε2/parenleftbigg/integraldisplayc1ε1
0k(ε)dε+/integraldisplayc2ε2
c1ε1(a2ε+b2)dε/parenrightbigg
=1
c2ε2/parenleftbigg
c1ε1k(ε1)+1
2a2(c2
2ε2
2−c2
1ε2
1)+b2(c2ε2−c1ε1)/parenrightbigg
=1
c2ε2/parenleftbigg
c1ε1k(ε1)+1
2a2(c2ε2−c1ε1)2+(a1ε2+b1)(c2ε2−c1ε1)/parenrightbigg
=1
c2ε2(c1ε1k(ε1)+c1ε1(a1ε2+b1−k(ε1))+(a1ε2+b1)(c2ε2−c1ε1))
=a1ε2+b1=Gz(ε2) = VaR ε2(X)
Hence, (2) is satisﬁed, and Π X(ε1) =c1and Π X(ε2) =c2.
Therefore, it is checked that Xsatisﬁes Π X(ε1) =c1and Π X(ε2) =c2for all ﬁve cases.
The following propositions address the issue discussed in Remark 1by showing that the boundary
cases of ( ε1,c1,ε2,c2) cannot be achieved by strictly decreasing quantile functions, and hence our
construction of quantiles with a ﬂat region in Figure 5are needed.
Proposition 6. For anyX∈L1, letε1,ε2∈(0,1)be such that E[X]/lessorequalslantVaRε2(X)andε1< ε2. Then,
ΠX(ε2) = max{1,ΠX(ε1)ε1/ε2}if and only if VaRε1(X) = VaR ε2(X).
Proof.Using the same logic as in Lemma 1, we have that Π X(ε1) and Π X(ε2) are ﬁnite.
We ﬁrst show the “if” statement. Assume VaR ε1(X) = VaR ε2(X). As VaR ε(X) is decreasing, we
know that VaR ε(X) is a constant on [ ε1,ε2].
If VaR ε(X) = VaR ε1(X) forε∈(0,ε1), then VaR ε(X) is a constant on (0 ,ε2]. Therefore, we
can get Π X(ε1) = Π X(ε2) = 1. Note that Π X(ε1)ε1/ε2=ε1/ε2<1. Thus, we obtain Π X(ε2) =
max{1,ΠX(ε1)ε1/ε2)}.
If there exists ε∈(0,ε1) such that VaR ε(X)>VaRε1(X), then ES ε(X) is strictly decreas-
ing on [ε1,1]. By the equivalent condition between VaR and ES, VaR ε1(X) = VaR ε2(X) implies
ESε1ΠX(ε1)(X) = ES ε2ΠX(ε2)(X). Thus, ε1ΠX(ε1) =ε2ΠX(ε2). Furthermore, we have
VaRε1ΠX(ε1)(X)<ESε1ΠX(ε1)(X) = VaR ε1(X) = VaR ε2(X).
Thus,ε1ΠX(ε1)> ε2and we get Π X(ε2) = max {1,ΠX(ε1)ε1/ε2}.
Next, we show the “only if” statement. Assume Π X(ε2) = max{1,ΠX(ε1)ε1/ε2}.
If ΠX(ε2) = 1, then VaR ε2(X) = ES ε2(X). This implies that VaR ε(X) is a constant on (0 ,ε2],
which gives VaR ε1(X) = VaR ε2(X).
36If ΠX(ε2) = ΠX(ε1)ε1/ε2, thenε2ΠX(ε2) =ε1ΠX(ε1). Hence, we have
VaRε1(X) = ES ε1ΠX(ε1)(X) = ES ε2ΠX(ε2)(X) = VaR ε2(X).
Thus, we complete the proof.
Proposition 7. For any X∈L1, letε1,ε2∈(0,1)be such that E[X]/lessorequalslantVaRε2(X)andε1< ε2. Let
c1= ΠX(ε1)andc2= ΠX(ε2). IfVaRε1(X)>VaRε2(X), then
ˆc/lessorequalslantc2/lessorequalslant

min/braceleftbigg1
ε2,c1ε1
ε2/parenleftbiggVaRε1(X)−VaRc1ε1(X)
VaRε2(X)−VaRc1ε1(X)/parenrightbigg/bracerightbigg
,VaRc1ε1(X)<VaRε2(X),
1
ε2, VaRc1ε1(X)/greaterorequalslantVaRε2(X),
where
ˆc= inf/braceleftbigg
t∈(1,1/ε2] :(tε2−c1ε1)(VaR ε2(X)−VaRtε2(X))
c1ε1(VaRε1(X)−VaRε2(X))/greaterorequalslant1/bracerightbigg
.
Moreover, ˆc/greaterorequalslantmax{1,c1ε1/ε2}.
Proof.AsE[X]/lessorequalslantVaRε2(X), we have c1<∞andc2<∞. By deﬁnition, c2/lessorequalslant1/ε2. From Lemma 6,
we getc2>max{1,c1ε1/ε2}. Thus, the value of c2should be in (max {1,c1ε1/ε2},1/ε2].
Note that c1,ε1,c2,ε2satisfy the equivalent condition ( 2). We can rewrite ( 2) as
/integraldisplayc1ε1
0VaRε(X)dε=c1ε1VaRε1(X) and/integraldisplayc2ε2
0VaRε(X)dε=c2ε2VaRε2(X).
Therefore, we have/integraldisplayc2ε2
c1ε1VaRε(X)dε=c2ε2VaRε2(X)−c1ε1VaRε1(X).
Furthermore, by the monotonicity of VaR, we have
(c2ε2−c1ε1)VaRc2ε2(X)/lessorequalslant/integraldisplayc2ε2
c1ε1VaRε(X)dε/lessorequalslant(c2ε2−c1ε1)VaRc1ε1(X).
The two inequality will provide an upper bound and a lower bound for c2.
An upper bound on c2. Usingc2ε2VaRε2(X)−c1ε1VaRε1(X)/lessorequalslant(c2ε2−c1ε1)VaRc1ε1(X),we have
c2ε2(VaRε2(X)−VaRc1ε1(X))/lessorequalslantc1ε1(VaRε1(X)−VaRc1ε1(X)). (9)
If VaR c1ε1(X)/greaterorequalslantVaRε2(X), the left side of ( 9) is less or equal to 0 and the right side of ( 9)
is larger or equal to 0 because VaR ε1(X)/greaterorequalslantVaRc1ε1(X). Therefore, ( 9) is satisﬁes for any c2∈
(max{1,c1ε1/ε2},1/ε2]. The upper bound for c2is unchanged.
37On the other hand, if VaR c1ε1(X)<VaRε2(X), we have
c2/lessorequalslantc1ε1
ε2/parenleftbiggVaRε1(X)−VaRc1ε1(X)
VaRε2(X)−VaRc1ε1(X)/parenrightbigg
.
Thus, an upper bound for c2is min/braceleftBig
1
ε2,c1ε1
ε2/parenleftBigVaRε1(X)−VaRc1ε1(X)
VaRε2(X)−VaRc1ε1(X)/parenrightBig/bracerightBig
.
A lower bound on c2. It holds that
(c2ε2−c1ε1)VaRc2ε2(X)/lessorequalslantc2ε2VaRε2(X)−c1ε1VaRε1(X).
Subtracting ( c2ε2−c1ε1)VaRε2(X) from both sides, we get
(c2ε2−c1ε1)(VaR ε2(X)−VaRc2ε2(X))/greaterorequalslantc1ε1(VaRε1(X)−VaRε2(X)). (10)
Fort∈(0,1/ε2), let
f(t) = (tε2−c1ε1)(VaR ε2(X)−VaRtε2(X)).
As we can see, f(1) = 0, f(c1ε1/ε2) = 0 and f(t)/lessorequalslant0 ift∈[min{1,c1ε1/ε2},max{1,c1ε1/ε2}]. Thef
is increasing in the interval (max {1,c1ε1/ε2},1/ε2), decreasing in (0 ,min{1,c1ε1/ε2}). Hence, by ( 10),
the lower bound for c2is
ˆc= inf/braceleftbigg
t∈(1,1/ε2] :(tε2−c1ε1)(VaR ε2(X)−VaRtε2(X))
c1ε1(VaRε1(X)−VaRε2(X))/greaterorequalslant1/bracerightbigg
.
Asc1ε1(VaRε1(X)−VaRε2(X))>0, we have ˆ c/greaterorequalslantmax{1,c1ε1/ε2}.
B Omitted proofs in Section 4.4
Proof of Theorem 2.By Proposition 3, for any X∈ X, we can ﬁnd f∈ Csatisfying ( 3) such that
zf(y) = 1/πX(y) =candX=f(U). Asz(y) =cis a continuously diﬀerentiable function, we know
that all such fis characterizedby the advanced diﬀerential equation ( 4). First, we show for any strictly
decreasing solution fto (4) can be represented as
f(y) =C0+C1yα+O/parenleftbig
yζ/parenrightbig
.
Let us start with ( 4). Ifz(y) =c, we need to solve ffrom
f(y) =f(cy)+cyf′(cy), y∈(0,1].
Even though fin the ﬁrst place is considered on (0 ,1], given that c <1, and this ﬁnal equation, one
38can expand it to the whole positive line:
f(y) =f(cy)+cyf′(cy), y >0.
Next, let x(t) =e−tf(e−t) fort∈Randa=−log(c)>0. This is equivalent to say that f(y) =
x(−log(y))/y. This changing variable simply gives the following delayed diﬀerential eq uation:
x′(t) =−e−ax(t−a), t∈R.
Since we have assumed that fis strictly decreasing, i.e., f′<0, we have an extra restriction on x.
Note that
x′(t) =−e−tf/parenleftbig
e−t/parenrightbig
−e−2tf′/parenleftbig
et/parenrightbig
=−x(t)−e−2tf′/parenleftbig
et/parenrightbig
.
Thus, we have f′<0⇔x′+x >0. Therefore, we are looking for a solution to the following delay
diﬀerential equation (DDE):


x′(t) =−e−ax(t−a),
x′(t)+x(t)>0,t∈R. (11)
A standard approach of ﬁnding the solutions is to assume that they are in the form of a characteristic
function t/ma√sto→emt. Putting this solution inside the equation, we get
memt=−e−aem(t−a)=⇒ameam= (−a)e(−a).
This means any solution is given by x(t) =emtwheremsolves the characteristic equation
l(ma) =l(−a), (12)
wherel(x) =xex. Letb=l(−a). Asa >0, we have b∈[−1/e,0). This equation has one obvious real
solution at m1=−1. To ﬁnd m, we need to know about the inverse of l. The inverse of the function
lis known as the Lambert Wfunction and plays an essential role in solving delayed and advanced
diﬀerential equations.
From the Lambert Wfunction, we know that l(z) =zez=bhas two real solutions when b∈
(−1/e,0) and one real solution when b=−1/e. As illustrated by Figure 18, if 0< c <1/e, the two
real solutions are z1=−a <−1 andz2=m2a >−1; thus,−1< m2<0. If 0< c <1/e, the two real
solutions are −1< z1=−a <0 andz2=m2a <−1; thus,m2<−1. Ifc= 1/e, there is only one real
solution z1=z2=−1; thusm2=m1=−1.
39-4 -3 -2 -1 1 2 3 4
-7-6-5-4-3-2-11
Figure 18: Lambert Wfunction.
It is important to note that in general an equation like l(z) =zez=bhas inﬁnite complex roots.
Letz=θ+iη, andb∈[−1/e,0). In that regard, we have
b=zez= (θ+iη)eθ+iη
= (θ+iη)(cos(η)+isin(η))
= (θcos(η)−ηsin(η))+i(θsin(η)+ηcos(η)).
This implies that θsin(η)+ηcos(η) = 0, and b=eθ(θcos(η)−ηsin(η)), leading to
η= 0,b=θeθorθ=−η
tan(η),b=−ηexp/parenleftBig
−η
tan(η)/parenrightBig
sin(η).
We plot the curves b=θeθand/parenleftbigg
−ηexp(−η
tan(η))
sin(η),−η
tan(η)/parenrightbigg
to ﬁnd out the relation between band the
real part of the solution in Figure 19. Thex-axis isband they-axis isθ. The blue curve is associated
withb=θeθ, which is essentially the principle branch of the Lambert Wfunction. For any b, one
can ﬁnd the real values of the roots by ﬁxing b. For instance, the green dashed line is associated with
b=−0.12. As one can see, the curves intersect this line in inﬁnite negative v alues. For b∈[−1/e,0),
we can see that the real roots are greater than the real part of the complex roots. For more explanation
of this, see Siewert and Burniston (1973).
40-4 -3 -2 -1 1 2 3 4
-7-6-5-4-3-2-112
Figure 19: The real part of the Lambert Wroots.
41Now assume that all the complex solutions for ( am)eam= (−a)e(−a)aremk=λk+σkifor
k= 1,2,3,..., where ( λ1,σ1) = (−1,0) and (λ2,σ2) = (m2,0). Based on the above discussions, we
have
λ1=−1> λ2=m2> λ3> λ4> ...whenc∈(1/e,1),
0> λ2=m2> λ1=−1> λ3> λ4> ...whenc∈(0,1/e),
and
λ1=λ2=−1> λ3> λ4> ...whenc= 1/e.
Let
C=


λ−σ
σ λ
=λ+σi|λ,σ∈R


be the set of all complex numbers. Then,
xC(t) = exp


λ−σ
σ λ
t


is a complex solution that solves ( 11). It is clear that ( 11) still holds for the linear transform of x(t).
Therefore, for any two 2 ×1 vector AandB,
x(t) =A′xC(t)B=eλt(C1cos(σt)+C2sin(σt))
is also a solution to ( 11).
InBellman and Cooke (1963), it is shown that all complex solutions to ( 11) can be represented
as follows:
xC(t) =∞/summationdisplay
k=1Ckemkt.
Putting it in the real-valued context, we have that all real-valued so lutions are in the following form:
x(t) =C1e−t+C2em2t+∞/summationdisplay
k=3eλkt(Ck,1cos(σkt)+Ck,2sin(σkt)).
Now let us check x′+x >0. This means that C2,{Ck,1}k/greaterorequalslant3and{Ck,2}k/greaterorequalslant3for alltmust satisfy
x′(t)+x(t) = (1+ m2)C2em2t
+∞/summationdisplay
k=3eλkt((λkCk,1+σkCk,2+Ck,1)cos(σkt)+(λkCk,2−σkCk,1+Ck,2)sin(σkt))>0.
Asλk< m2fork/greaterorequalslant3, we have lim t→∞(x′(t)+x(t))/em2t= (1+m2)C2. Therefore, we need C2<0
42ifm2<−1 orC2>0 ifm2>−1. That is C2(1+m2)>0. Then the solution can be written as
x(t) =C1e−t+C2em2t+O/parenleftbig
eλ3t/parenrightbig
.
By a change of variable, we get
f(y) =C1+C2yα+O/parenleftbig
yζ/parenrightbig
,
whereα=−(1+m2) andζ=−(1+λ3). Asλ3<min{−1,m2}andC2(1 +m2)>0, we have
ζ >max{0,α}andC2α <0. Also note that since m2solves (am)eam= (−a)e(−a), by replacing
m2=−1−αanda=−log(c), we get ( α+1)−1/α=c.
C Omitted proofs in Section 5
Proof of Proposition 4.Before proving the statements in the proposition, we introduce th e following
linking function, for X∈ X,
ΓX(ε) = 1−FX(ESε(X)), ε∈[0,1].
AsX∈Xit is easy to check that Γ Xsatisﬁes Assumption 1for anyX∈ X. The domain of Γ X(ε) is
[0,1] and its range is [0 ,1−FX(E[X])].
As ES ε(X) = VaR ΓX(ε)(X), we have
VaRΓX(ε)(X) = ES ε(X) = VaR ε/πX(ε)(X) forε∈(0,1].
Hence we havethe simple relationshipΓ X(ε) =ε/πX(ε).Therefore, Π X(ε) =πX/parenleftbig
Γ−1
X(ε)/parenrightbig
andπX(ε) =
ΠX(ΓX(ε)). The function Γ Xyields an associationbetween a point on the PELVE on (0 ,1−FX(E[X])]
and a point on the dual PELVE curve on (0 ,1] with the same value. Furthermore, we have πXis
continuous on (0 ,1) asπX(ε) =ε/ΓX(ε) and Γ Xis continuous.
Next, we show the statements (i)-(iv). The equivalence (i) of mono tonicity of Π Xand that of
πX(·) follows from Π X(ε) =πX/parenleftbig
Γ−1
X(ε)/parenrightbig
,πX(ε) = ΠX(ΓX(ε)) and that Γ Xis increasing.
For (ii), (iii) and (iv), we ﬁrst show that Γ Xis location-scale invariant and shape relevant (in the
sense of ( 13)). Assume that f:R→Ris a strictly increasing concave function such that f(X)∈ X.
By Jensen’s inequality and the dual representation of ES p, we have
ESp(f(X))/lessorequalslantf(ESp(X))
43for allp∈(0,1). This statement can be found in Appendices A.2 in Li and Wang (2022). Therefore,
Γf(X)(ε) = 1−Ff(X)(ESε(f(X)))
/greaterorequalslant1−Ff(X)(f(ESε(X))) = 1−FX(ESε(X)) = Γ X(ε).(13)
Then, wehaveΓ f(X)(ε)/greaterorequalslantΓX(ε)forallstrictlyincreasingconcavefunctions: f:R→Rwithf(X)∈ X.
For any strictly increasing convex function g:R→Rwithg(X)∈ X, we can take f(x) =g−1(X),
which is a strictly increasing concave function. Therefore, we have Γg(X)(ε)/lessorequalslantΓX(ε) for all strictly
increasing convex functions g.
Forλ >0 anda∈R, we have that f(x) =λX+ais both convex and concave. Therefore,
ΓλX+a(ε) = ΓX(ε) for allε∈[0,1]. In conclusion, we have the following results for Γ.
(1) For all λ >0 anda∈R, ΓλX+a(ε) = ΓX(ε).
(2) Γf(X)(ε)/greaterorequalslantΓX(ε) for all strictly increasing concave functions: f:R→Rwithf(X)∈ X.
(3) Γg(X)(ε)/lessorequalslantΓX(ε) for all strictly increasing convex functions: g:R→Rwithg(X)∈ X.
Then, we have (ii), (iii) and (iv) from πX(ε) =ε/ΓX(ε).
Proof of Theorem 3.Theideaistoprovethatif1 /ηisconvex(concave),then x/ma√sto→F−1((1−p)F(x)+p)
is convex (concave) for all p∈(0,1). Then, we can get the desired result by Proposition 5. We will
use the following steps to show this statement.
Step 1.Lets(x) = log(1 −F(x)) forx∈(ess-inf(X),ess-sup(X)). Then, sis a continuous and
strictly decreasing function and s(x)<0. Lets−1be the inverse function of s. Now, we have
F(x) = 1−es(x), x∈(ess-inf(X),ess-sup(X))
and
F−1(t) =s−1(log(1−t)), t∈(0,1).
Therefore,
F−1/parenleftbig
(1−p)F(x)+p/parenrightbig
=s−1/parenleftbig
log(1−(1−p)F(x)−p)/parenrightbig
=s−1/parenleftBig
log/parenleftbig
1−F(x)/parenrightbig
+log(1−p)/parenrightBig
=s−1/parenleftBig
log/parenleftbig
es(x)/parenrightbig
+log(1−p)/parenrightBig
=s−1/parenleftBig
s(x)+log(1 −p)/parenrightBig
.
Letθ= log(1−p). It follows that the statement that x/ma√sto→F−1/parenleftbig
(1−p)F(x)+p/parenrightbig
is convex (concave) for
allp∈(0,1) is equivalent to the statement that x/ma√sto→s−1(s(x)+θ) is convex (concave) for all θ <0.
44Step 2.Letg(x) :=−s−1(x). Then, gis strictly increasing. We will show that if 1 /ηis convex
(concave), log( g′(x)) is convex (concave).
Asg(x) =−s−1(x) =−S−1(ex),we have
g′(x) =ex
f(S−1(ex)).
LetH(x) := log(g′(x)) =x−log/parenleftbig
f/parenleftbig
S−1(ex)/parenrightbig/parenrightbig
. We have
H(log(S(x))) = log S(x)−logf(x) =−logη(x). (14)
Then, taking the derivative on both sides of ( 14), we get
−H′/parenleftbig
log(S(x))/parenrightbig
η(x) =−η′(x)
η(x)
⇐⇒H′/parenleftbig
log(S(x))/parenrightbig
=η′(x)
η2(x)=−d
dx/parenleftbigg1
η(x)/parenrightbigg
.
Taking a derivative in both sides again, we get
−H′′/parenleftbig
log(S(x))/parenrightbig
η(x) =−d2
dx2/parenleftbigg1
η(x)/parenrightbigg
.
Then, 1/ηis a convex (concave) function means H′′(x)/greaterorequalslant0 (H′′(x)/lessorequalslant0), which gives that log g′(x) is
convex (concave).
Step 3.Forθ <0, letGθ(x) :=s−1(s(x)+θ). We are going to show
lim
z→0Gθ(x+z)−Gθ(x)
z/lessorequalslantlim
z→0Gθ(x′+z)−Gθ(x′)
z(15)
for allx < x′.
We take z >0 ﬁrst. As sis strictly decreasing, s−1is also strictly decreasing. Then, Gθis a
continuous and strictly increasing function. As θ <0, we also have Gθ(x)> x. Take arbitrary x,x′,y
andzsuch that x < x′,x < yandz >0. Letθ=s(y)−s(x). Then, we have Gθ(x) =y. Deﬁne
h=Gθ(x+z)−y, y′=Gθ(x′) and h′=Gθ(x′+z)−y′.
By the deﬁnition of Gθ, we have s(y+h) =s(x+z)+θ,s(y′) =s(x′)+θands(y′+h′) =s(x′+z)+θ.
As a result, we have
s(y+h)−s(y) =s(x+z)−s(x) and s(y′+h′)−s(y′) =s(x′+z)−s(x′).
45By the mean-value theorem, there exists ζ∈(y,y+h),ζ′∈(y′,y′+h′),ξ∈(x,x+z) and
ξ′∈(x′,x′+z) such that
s′(ζ)h=s′(ξ)zands′(ζ′)h′=s′(ξ′)z.
Furthermore, x,x′,yandy′satisfyx < x′< y′andx < y < y′. Ifzis small enough, then handh′
will also be small enough as Gθis continuous. Therefore, we have ξ < ξ′< ζ′andξ < ζ < ζ′whenz
is small enough.
In Step 2, we have that log g′(x) is convex when 1 /ηis convex. Therefore, we get
log(g′(a))+log(g′(b))/greaterorequalslantlog(g′(a′))+log(g′(b′)),
for alla < a′< banda < b′< b, which means
g′(a)g′(b)/greaterorequalslantg′(a′)g′(b′).
Asg(x) =−s−1(x), we have
1
s′(s−1(a))s′(s−1(b))/greaterorequalslant1
s′(s−1(a′))s′(s−1(b′)).
Ass−1(x) is strictly decreasing, it means that
s′(α)s′(β)/lessorequalslants′(α′)s′(β′)
forα > α′> βandα > β′> β. Therefore, we have s′(ξ)s′(ζ′)/lessorequalslants′(ξ′)s′(ζ) asζ′> ζ > ξ and
ζ′> ξ′> ξ. That is,
h=s′(ξ)z
s′(ζ)/lessorequalslants′(ξ′)z
s′(ζ′)=h′.
On the other hand, h=Gθ(x+z)−Gθ(x) andh′=Gθ(x′+z)−Gθ(x′). Therefore,
Gθ(x+z)−Gθ(x)/lessorequalslantGθ(x′+z)−Gθ(x′)
whenzis small enough. If z <0, we can also get ( 15) by an analogous argument.
Hence, the second-order derivative of Gθis increasing for each θ <0, which means that x/ma√sto→
F−1/parenleftbig
(1−p)F(x)+p/parenrightbig
is convex for all p∈(0,1) if 1/ηis convex.
An analogous argument yields that x/ma√sto→F−1/parenleftbig
(1−p)F(x)+p/parenrightbig
is concave for all p∈(0,1) when
1/ηis concave.
46