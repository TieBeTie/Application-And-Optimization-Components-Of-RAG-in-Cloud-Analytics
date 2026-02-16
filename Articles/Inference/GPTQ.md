See also: [[Quantization]], [[Layer-wise Quantization]], [[OBQ]], [[GPTQ Algorithm]], [[Hessian Matrix]], [[Cholesky Decomposition]]

#article #gptq #quantization

---

Published as a conference paper at ICLR 2023
## GPTQ: ACCURATEPOST-TRAININGQUANTIZATION
## FORGENERATIVEPRE-TRAINEDTRANSFORMERS
## Elias Frantar
## ∗
IST Austria
## Saleh Ashkboos
ETH Zurich
## Torsten Hoefler
ETH Zurich
## Dan Alistarh
IST Austria & NeuralMagic
## ABSTRACT
Generative  Pre-trained  Transformer  models,  known  as  GPT  or  OPT,  set  them-
selves apart through breakthrough performance across complex language mod-
elling  tasks,  but  also  by  their  extremely  high  computational  and  storage  costs.
Specifically, due to their massive size, even inference for large, highly-accurate
GPT models may require multiple performant GPUs, which limits the usability
of  such  models.   While  there  is  emerging  work  on  relieving  this  pressure  via
model compression,  the applicability and performance of existing compression
techniques is limited by the scale and complexity of GPT models.  In this paper,
we address this challenge, and propose GPTQ, a new one-shot weight quantiza-
tion method based on approximate second-order information, that is both highly-
accurate and highly-efficient. Specifically, GPTQ can quantize GPT models with
175 billion parameters in approximately four GPU hours, reducing the bitwidth
down to 3 or 4 bits per weight, with negligible accuracy degradation relative to the
uncompressed baseline. Our method more than doubles the compression gains rel-
ative to previously-proposed one-shot quantization methods, preserving accuracy,
allowing us for the first time to execute an 175 billion-parameter model inside a
single GPU for generative inference.  Moreover, we also show that our method
can still provide reasonable accuracy in theextreme quantizationregime, in which
weights are quantized to 2-bit or eventernaryquantization levels.  We show ex-
perimentally that these improvements can be leveraged for end-to-end inference
speedups over FP16, of around 3.25x when using high-end GPUs (NVIDIA A100)
and 4.5x when using more cost-effective ones (NVIDIA A6000). The implemen-
tation is available athttps://github.com/IST-DASLab/gptq.
## 1INTRODUCTION
Pre-trained generative models from the Transformer (Vaswani et al., 2017) family, commonly known
as GPT or OPT (Radford et al., 2019; Brown et al., 2020; Zhang et al., 2022), have shown break-
through performance for complex language modelling tasks, leading to massive academic and prac-
tical interest.  One major obstacle to their usability is computational and storage cost, which ranks
among the highest for known models. For instance, the best-performing model variants, e.g. GPT3-
175B, have in the order of 175 billion parameters and require tens-to-hundreds of GPU years to
train (Zhang et al., 2022).  Even the simpler task of inferencing over a pre-trained model, which is
our focus in this paper, is highly challenging:  for instance, the parameters of GPT3-175B occupy
326GB (counting in multiples of 1024) of memory when stored in a compact float16 format.  This
exceeds the capacity of even the highest-end single GPUs, and thus inference must be performed
using more complex and expensive setups, such as multi-GPU deployments.
Although a standard approach to eliminating these overheads ismodel compression, e.g. (Hoefler
et al., 2021; Gholami et al., 2021), surprisingly little is known about compressing such models for
inference.  One reason is that more complex methods for low-bitwidth quantization or model prun-
ing usually requiremodel retraining, which is extremely expensive for billion-parameter models.
Alternatively,post-trainingmethods (Nagel et al., 2020; Wang et al., 2020; Hubara et al., 2020;
Nahshan et al., 2021), which compress the model in one shot, without retraining, would be very
appealing. Unfortunately, the more accurate variants of such methods (Li et al., 2021; Hubara et al.,
2021; Frantar et al., 2022) are complex and challenging to scale to billions of parameters (Yao et al.,
## ∗
Corresponding author:elias.frantar@ist.ac.at
## 1
arXiv:2210.17323v2  [cs.LG]  22 Mar 2023

Published as a conference paper at ICLR 2023
2022).   To date,  only basic variants of round-to-nearest quantization (Yao et al., 2022; Dettmers
et al., 2022) have been applied at the scale of GPT-175B; while this works well for low compression
targets, e.g., 8-bit weights, they fail to preserve accuracy at higher rates.  It therefore remains open
whether one-shotpost-training quantizationto higher compression rates is generally-feasible.
## 10
## 1
## 10
## 0
## 10
## 1
## 10
## 2
#params in billions
## 5
## 10
## 15
## 20
## 25
## 30
## 35
## 40
## 45
## 50
Perplexity on WikiText2
## 110.
OPT Model Family
4bit RTN
4bit GPTQ
## FP16
## 10
## 0
## 10
## 1
## 10
## 2
#params in billions
## 10
## 20
## 30
## 40
## 50
## 60
Perplexity on WikiText2
## 571.
BLOOM Model Family
3bit RTN
3bit GPTQ
## FP16
Figure 1:  Quantizing OPT models to 4 and BLOOM models to 3 bit precision, comparing GPTQ
with the FP16 baseline and round-to-nearest (RTN) (Yao et al., 2022; Dettmers et al., 2022).
Contribution.In this paper, we present a new post-training quantization method, called GPTQ,
## 1
which is efficient enough to execute on models with hundreds of billions of parameters in at most
a  few  hours,  and  precise  enough  to  compress  such  models  to  3  or  4  bits  per  parameter  without
significant loss of accuracy. For illustration, GPTQ can quantize the largest publicly-available mod-
els,  OPT-175B and BLOOM-176B, in approximately four GPU hours,  with minimal increase in
perplexity, known to be a very stringent accuracy metric.
Further, we show that our model can also provide robust results in theextreme quantizationregime,
in which models are quantized to 2 bits per component, or eventernary values.  On the practical
side, we develop an execution harness which allows us to execute the resulting compressed models
efficiently for generative tasks.  Specifically, we are able to run the compressed OPT-175B model
for the first time on a single NVIDIA A100 GPU, or using only two more cost-effective NVIDIA
A6000 GPUs. We also implement bespoke GPU kernels which are able to leverage compression for
faster memory loading, resulting in speedups of≈3.25×when using A100 GPUs, and4.5×when
using A6000 GPUs.
To our knowledge, we are the first to show that extremely accurate language models with hundreds
of billions of parameters can be quantized to 3-4 bits/component: priorpost-training methodsonly
remain accurate at 8 bits (Yao et al., 2022; Dettmers et al., 2022), while priortraining-basedtech-
niques have only tackled models that are smaller by one to two orders of magnitude (Wu et al., 2022).
This high degree of compression may appear natural, as these networks are overparametrized; yet,
as we discuss in our detailed analysis of results, compression induces non-trivial tradeoffs between
the accuracy of the language modeling (perplexity), bit-width, and the size of the original model.
We hope that our work will stimulate further research in this area, and can be a further step towards
making these models available to a wider audience.  In terms of limitations, our method currently
does not provide speedups for the actual multiplications, due to the lack of hardware support for
mixed-precision operands (e.g.  FP16 x INT4) on mainstream architectures.  Moreover, our current
results do not include activation quantization, as they are not a significant bottleneck in our target
scenarios; however, this can be supported using orthogonal techniques (Yao et al., 2022).
## 2RELATEDWORK
Quantization  methods  fall  broadly  into  two  categories:   quantization  during  training,  and  post-
training methods.   The former quantize models during typically extensive retraining and/or fine-
tuning,  using  some  approximate  differentiation  mechanism  for  the  rounding  operation  (Gholami
et al., 2021; Nagel et al., 2021).  By contrast, post-training (“one-shot”) methods quantize a pre-
## 1
This merges the name of the OPT model family with the abbreviation for post-training quantization (PTQ).
## 2

Published as a conference paper at ICLR 2023
trained model using modest resources, typically a few thousand data samples and a few hours of
computation.  Post-training approaches are particularly interesting for massive models, for which
full model training or even finetuning can be expensive. We focus on this scenario here.
Post-training Quantization.Most post-training methods have focused on vision models. Usually,
accurate  methods  operate  by  quantizing  either  individual  layers,  or  small  blocks  of  consecutive
layers.  (See Section 3 for more details.)  The AdaRound method (Nagel et al., 2020) computes a
data-dependent rounding by annealing a penalty term, which encourages weights to move towards
grid points corresponding to quantization levels.  BitSplit (Wang et al., 2020) constructs quantized
values bit-by-bit using a squared error objective on the residual error, while AdaQuant (Hubara et al.,
2021) performs direct optimization based on straight-through estimates.  BRECQ (Li et al., 2021)
introduces Fisher information into the objective, and optimizes layers within a single residual block
jointly.   Finally,  Optimal Brain Quantization (OBQ) (Frantar et al., 2022) generalizes the classic
Optimal Brain Surgeon (OBS) second-order weight pruning framework (Hassibi et al., 1993; Singh
& Alistarh, 2020; Frantar et al., 2021) to apply to quantization. OBQ quantizes weights one-by-one,
in order of quantization error, always adjusting the remaining weights. While these approaches can
produce good results for models up to≈100million parameters in a few GPU hours, scaling them
to networks orders of magnitude larger is challenging.
Large-model  Quantization.With  the  recent  open-source  releases  of  language  models  like
BLOOM (Laurenc ̧on et al., 2022) or OPT-175B (Zhang et al., 2022), researchers have started to
develop affordable methods for compressing such giant networks for inference.   While all exist-
ing works—ZeroQuant (Yao et al., 2022), LLM.int8() (Dettmers et al., 2022), and nuQmm (Park
et al., 2022)— carefully select quantization granularity, e.g., vector-wise, they ultimately just round
weights to the nearest (RTN) quantization level, in order to maintain acceptable runtimes for very
large models.  ZeroQuant further proposes layer-wise knowledge distillation, similar to AdaQuant,
but the largest model it can apply this approach to has only 1.3 billion parameters.  At this scale,
ZeroQuant already takes≈3hours of compute; GPTQ quantizes models 100×larger in≈4hours.
LLM.int8()  observes  thatactivation  outliersin  a  few  feature  dimensions  break  the  quantization
of larger models,  and proposes to fix this problem by keeping those dimensions in higher preci-
sion. Lastly, nuQmm develops efficient GPU kernels for a specific binary-coding based quantization
scheme.
Relative to this line of work, we show that a significantly more complex and accurate quantizer can
be implemented efficiently at large model scale. Specifically, GPTQ more than doubles the amount
of compression relative to these prior techniques, at similar accuracy.
## 3BACKGROUND
Layer-Wise Quantization.At a high level,  our method follows the structure of state-of-the-art
post-training quantization methods (Nagel et al., 2020; Wang et al., 2020; Hubara et al., 2021; Fran-
tar et al., 2022), by performing quantization layer-by-layer, solving a corresponding reconstruction
problem for each layer. Concretely, letW
## `
be the weights corresponding to a linear layer`and let
## X
## `
denote the layer input corresponding to a small set ofmdata points running through the network.
Then, the objective is to find a matrix of quantized weights
## ̂
Wwhich minimizes the squared error,
relative to the full precision layer output. Formally, this can be restated as
argmin
## ̂
## W
## ||WX−
## ̂
## WX||
## 2
## 2
## .(1)
Further,  similar to (Nagel et al., 2020; Li et al., 2021; Frantar et al., 2022),  we assume that the
quantization grid for
## ̂
Wis fixed before the process, and that individual weights can move freely as
in (Hubara et al., 2021; Frantar et al., 2022).
Optimal  Brain  Quantization.Our  approach  builds  on  the  recently-proposed  Optimal  Brain
Quanization (OBQ) method (Frantar et al., 2022) for solving the layer-wise quantization problem
defined above, to which we perform a series of major modifications, which allow it to scale to large
language models, providing more thanthree orders of magnitudecomputational speedup.  To aid
understanding, we first briefly summarize the original OBQ method.
The OBQ method starts from the observation that Equation (1) can be written as the sum of the
squared errors, over each row ofW. Then, OBQ handles each rowwindependently, quantizing one
weight at a time while always updating all not-yet-quantized weights, in order to compensate for
the error incurred by quantizing a single weight.  Since the corresponding objective is a quadratic,
## 3

Published as a conference paper at ICLR 2023
whose Hessian isH
## F
## = 2X
## F
## X
## >
## F
, whereFdenotes the set of remaining full-precision weights,
the greedy-optimal weight to quantize next, which we denote byw
q
, and the corresponding optimal
update of all weights inF, denoted byδ
## F
, are given by the following formulas, where quant(w)
roundswto the nearest value on the quantization grid:
w
q
## =argmin
w
q
## (quant(w
q
## )−w
q
## )
## 2
## [H
## −1
## F
## ]
qq
## ,δ
## F
## =−
w
q
## −quant(w
q
## )
## [H
## −1
## F
## ]
qq
## ·(H
## −1
## F
## )
## :,q
## .(2)
OBQ quantizes weights iteratively using these two equations, until all the weights ofware quan-
tized. This is done efficiently, avoiding expensive full recomputations ofH
## −1
, by removing theqth
row and column ofH, which is necessary after quantizingw
q
, directly in the inverse via one step of
Gaussian elimination. Namely, the updated inverse is given by the formula
## H
## −1
## −q
## =
## (
## H
## −1
## −
## 1
## [H
## −1
## ]
qq
## H
## −1
## :,q
## H
## −1
q,:
## )
## −p
## .(3)
This method comes with a vectorized implementation,  handling multiple rows ofWin parallel.
Eventually, the algorithm can achieve reasonable runtimes on medium-sized models: for instance, it
can fully quantize the ResNet-50 model (25M parameters) in≈1hour on a single GPU, which is
roughly in line with other post-training methods achieving state-of-the-art accuracy (Frantar et al.,
2022). However, the fact that OBQ’s runtime for ad
row
## ×d
col
matrixWhascubicinput dependency
## O(d
row
## ·d
## 3
col
)means that applying it to models with billions of parameters is extremely expensive.
## 4THEGPTQ ALGORITHM
Step 1: Arbitrary Order Insight.As explained in the previous section, OBQ quantizes weights in
greedy order, i.e. it always picks the weight which currently incurs the least additional quantization
error. Interestingly, we find that, while this quite natural strategy does indeed seem to perform very
well, its improvement over quantizing the weights in arbitrary order is generally small, in particular
on  large,  heavily-parametrized  layers.   Most  likely,  this  is  because  the  slightly  lower  number  of
quantized  weights  with  large  individual  error  is  balanced  out  by  those  weights  being  quantized
towards the end of the process, when only few other unquantized weights that can be adjusted for
compensation remain.  As we will now discuss, this insight thatany fixed order may perform well,
especially on large models, has interesting ramifications.
## Inverse Layer Hessian
(Cholesky Form)
computed initially
block i quantized recursively
column-by-column
## Weight Matrix / Block
unquantized weights
that are updated
quantized weights
Figure 2: GPTQ quantization procedure. Blocks
of consecutivecolumns(bolded) are quantized at
a given step, using the inverse Hessian informa-
tion stored in the Cholesky decomposition,  and
the remaining weights (blue) are updated at the
end  of  the  step.   The  quantization  procedure  is
applied recursively inside each block:  the white
middle column is currently being quantized.
The original OBQ method quantizes rows ofW
independently, in a specific order defined by the
corresponding errors.  By contrast, we will aim
to quantize the weights ofall rows in the same
order,  and  will  show  that  this  typically  yields
results  with  a  final  squared  error  that  is  simi-
lar to the original solutions.  As a consequence,
the set of unquantized weightsFand similarly
## H
## −1
## F
is always the same for all rows (see Fig-
ure 2 for an illustration).  In more detail, the lat-
ter is due to the fact thatH
## F
depends only on
the layer inputsX
## F
, which are the same for all
rows,  and  not  on  any  weights.   Therefore,  we
have  to  perform  the  update  ofH
## −1
## F
given  by
Equation (3) onlyd
col
times, once per column,
rather thand
row
## ·d
col
times, once per weight. This
reduces the overall runtime fromO(d
row
## ·d
## 3
col
## )
toO(max{d
row
## ·d
## 2
col
## ,d
## 3
col
}), i.e., by a factor of
min{d
row
## ,d
col
}.  For larger models, this differ-
ence  consists  of  several  orders  of  magnitude.
However, before this algorithm can actually be
applied to very large models in practice, two ad-
ditional major problems need to be addressed.
Step 2:  Lazy Batch-Updates.First, a direct implementation of the scheme described previously
will not be fast in practice, because the algorithm has a relatively low compute-to-memory-access
ratio. For example, Equation (3) needs to update all elements of a potentially huge matrix using just a
## 4

Published as a conference paper at ICLR 2023
few FLOPs for each entry. Such operations cannot properly utilize the massive compute capabilities
of modern GPUs, and will be bottlenecked by the significantly lower memory bandwidth.
Fortunately, this problem can be resolved by the following observation: The final rounding decisions
for columniare only affected by updates performed on this very column, and so updates to later
columns are irrelevant at this point in the process.  This makes it possible to “lazily batch” updates
together, thus achieving much better GPU utilization.  Concretely, we apply the algorithm toB=
128columns at a time, keeping updates contained to those columns and the correspondingB×B
block ofH
## −1
(see also Figure 2).  Only once a block has been fully processed, we perform global
updates of the entireH
## −1
andWmatrices using the multi-weight versions of Equations (2) and
(3) given below, withQdenoting a set of indices, andH
## −1
## −Q
denoting the inverse matrix with the
corresponding rows and columns removed:
δ
## F
## =−(w
## Q
## −quant(w
## Q
## ))([H
## −1
## F
## ]
## QQ
## )
## −1
## (H
## −1
## F
## )
## :,Q
## ,(4)
## H
## −1
## −Q
## =
## (
## H
## −1
## −H
## −1
## :,Q
## ([H
## −1
## ]
## QQ
## )
## −1
## H
## −1
## Q,:
## )
## −Q
## .(5)
Although this strategy does not reduce the theoretical amount of compute, it effectively addresses
the memory-throughput bottleneck.   This provides an order of magnitude speedup for very large
models in practice, making it a critical component of our algorithm.
Step 3: Cholesky Reformulation.The final technical issue we have to address is given by numeri-
cal inaccuracies, which can become a major problem at the scale of existing models, especially when
combined with the block updates discussed in the previous step.  Specifically, it can occur that the
matrixH
## −1
## F
becomes indefinite, which we notice can cause the algorithm to aggressively update the
remaining weights in incorrect directions, resulting in an arbitrarily-bad quantization of the corre-
sponding layer. In practice, we observed that the probability of this happening increases with model
size:  concretely, it almost certainly occurs for at least a few layers on models that are larger than
a few billion parameters.  The main issue appears to be the repeated applications of Equation (5),
which accumulate various numerical errors, especially through the additional matrix inversion.
For smaller models, applying dampening, that is adding a small constantλ(we always choose 1% of
the average diagonal value) to the diagonal elements ofHappears to be sufficient to avoid numerical
issues. However, larger models require a more robust and general approach.
To address this, we begin by noting that the only information required fromH
## −1
## F
q
, whereF
q
denotes
the set of unquantized weights when quantizing weightq, is rowq, or more precisely, the elements in
this row starting with the diagonal. The consequence is that we could precompute all of these rows
using a more numerically-stable method without any significant increase in memory consumption.
Indeed, the row removal via (3) for our symmetricH
## −1
essentially corresponds to taking a Cholesky
decomposition, except for the minor difference that the latter divides rowqby([H
## −1
## F
q
## ]
qq
## )
## 1/2
## . Hence,
we can leverage state-of-the-art Cholesky kernels to compute all information we will need fromH
## −1
upfront. In combination with mild dampening, the resulting method is robust enough to execute on
huge models without issues. As a bonus, using a well-optimized Cholesky kernel also yields further
speedup. We detail all small changes necessary for the Cholesky version of the algorithm next.
The Full Algorithm.Finally, we present the full pseudocode for GPTQ in Algorithm 1, including
the optimizations discussed above.
Algorithm 1QuantizeWgiven inverse HessianH
## −1
## = (2XX
## >
+λI)
## −1
and blocksizeB.
## Q←0
d
row
## ×d
col
// quantized output
## E←0
d
row
## ×B
// block quantization errors
## H
## −1
←Cholesky(H
## −1
## )
## >
// Hessian inverse information
fori= 0, B,2B, . . .do
forj=i, . . . , i+B−1do
## Q
## :,j
←quant(W
## :,j
)// quantize column
## E
## :,j−i
## ←(W
## :,j
## −Q
## :,j
## )/[H
## −1
## ]
jj
// quantization error
## W
:,j:(i+B)
## ←W
:,j:(i+B)
## −E
## :,j−i
## ·H
## −1
j,j:(i+B)
// update weights in block
end for
## W
:,(i+B):
## ←W
:,(i+B):
## −E·H
## −1
i:(i+B),(i+B):
// update all remaining weights
end for
## 5

Published as a conference paper at ICLR 2023
## 5EXPERIMENTALVALIDATION
Overview.We begin our experiments by validating the accuracy of GPTQ relative to other accurate-
but-expensive quantizers, on smaller models, for which these methods provide reasonable runtimes.
Next, we examine GPTQ’s runtime scaling for very large models.  Then, we present 3- and 4-bit
quantization results for the entire BLOOM and OPT model families,  evaluated via perplexity on
challenging language generation tasks. In addition, we show that our method is also stable for 2-bit
quantization when the granularity is reduced to small blocks of consecutive weights. To complement
this perplexity analysis, we also evaluate the resulting quantized models on a series of standard zero-
shot tasks.  Finally, we focus on the two largest (and interesting) openly-available models, Bloom-
176B and OPT-175B, where we perform a detailed evaluation on several tasks. For these models, we
also present practical improvements, namely reducing the number of GPUs required for inference
as well as end-to-end speedups for generative tasks.
Setup.We implemented GPTQ in PyTorch (Paszke et al., 2019) and worked with the HuggingFace
integrations of the BLOOM (Laurenc ̧on et al., 2022) and OPT (Zhang et al., 2022) model families.
We quantized all models (including the 175 billion parameter variants)using a single NVIDIA A100
GPUwith 80GB of memory. Our entire GPTQ calibration data consists of 128 random 2048 token
segments from the C4 dataset (Raffel et al., 2020), i.e., excerpts from randomly crawled websites,
which  represents  generic  text  data.   We  emphasize  that  this  means  that  GPTQ  does  not  see  any
task-specific data, and our results thus remain actually “zero-shot”.  We perform standard uniform
per-row asymmetric quantization on the min-max grid, similar to Dettmers et al. (2022). Additional
evaluation details can be found in Appendix A.2.1.
To ensure that the entire compression procedure can be performed with significantly less GPU mem-
ory than what would be required to run the full precision model, some care must be taken.  Specif-
ically, we always load one Transformer block, consisting of 6 layers, at a time into GPU memory
and then accumulate the layer-Hessians and perform quantization. Finally, the current block inputs
are sent through the fully quantized block again to produce the new inputs for the quantization of
the next block. Hence, the quantization process operates not on the layer inputs in the full precision
model but on the actual layer inputs in the already partially quantized one.  We find that this brings
noticeable improvements at negligible extra cost.
Baselines.Our primary baseline, denoted by RTN, consists of rounding all weights to the nearest
quantized value on exactly the same asymmetric per-row grid that is also used for GPTQ, meaning
that it corresponds precisely to the state-of-the-art weight quantization of LLM.int8().  This is cur-
rently the method of choice in all works on quantization of very large language models (Dettmers
et al., 2022; Yao et al., 2022; Park et al., 2022): its runtime scales well to networks with many bil-
lions of parameters, as it simply performs direct rounding.  As we will also discuss further, more
accurate methods, such as AdaRound (Nagel et al., 2020) or BRECQ (Li et al., 2021), are currently
too slow for models with many billions of parameters, the main focus of this work.  Nevertheless,
we also show that GPTQ is competitive with such methods for small models, while scaling to huge
ones like OPT-175B as well.
Quantizing Small Models.As a first ablation study, we compare GPTQ’s performance relative to
state-of-the-art post-training quantization (PTQ) methods, on ResNet18 and ResNet50, which are
standard PTQ benchmarks, in the same setup as (Frantar et al., 2022).  As can be seen in Table 1,
GPTQ performs on par at 4-bit, and slightly worse than the most accurate methods at 3-bit.  At the
same time, it significantly outperforms AdaQuant, the fastest amongst prior PTQ methods. Further,
we compare against the full greedy OBQ method on two smaller language models: BERT-base (De-
vlin et al., 2019) and OPT-125M. The results are shown in Appendix Table 8. At 4 bits, both methods
perform similarly, and for 3 bits, GPTQ surprisingly performs slightly better.  We suspect that this
is because some of the additional heuristics used by OBQ, such as early outlier rounding, might
require careful adjustments for optimal performance on non-vision models. Overall, GPTQ appears
to be competitive with state-of-the-art post-training methods for smaller models, while taking only
<1minute rather than≈1hour. This enables scaling to much larger models.
Runtime.Next we measure the full model quantization time (on a single NVIDIA A100 GPU) via
GPTQ; the results are shown in Table 2.  As can be seen, GPTQ quantizes 1-3 billion parameter
models in a matter of minutes and 175B ones in a few hours.  For reference, the straight-through
based method ZeroQuant-LKD (Yao et al., 2022) reports a 3 hour runtime (on the same hardware)
for a 1.3B model, which would linearly extrapolate to several hundred hours (a few weeks) for 175B
## 6

Published as a conference paper at ICLR 2023
## Method
## RN18 – 69.76 %RN50 – 76.13%
## 4bit3bit4bit3bit
AdaRound69.3468.3775.8475.14
AdaQuant68.1259.2174.6864.98
## BRECQ69.3768.4775.8875.32
## OBQ69.5668.6975.7275.24
## GPTQ69.3767.8875.7174.87
Table  1:   Comparison  with  state-of-the-art
post-training methods for vision models.
## OPT13B30B66B175B
## Runtime20.9m44.9m1.6h4.2h
## BLOOM1.7B3B7.1B176B
## Runtime2.9m5.2m10.0m3.8h
Table 2: GPTQ runtime for full quantization
of the 4 largest OPT and BLOOM models.
models.  Adaptive rounding-based methods typically employ a lot more SGD steps and would thus
be even more expensive (Nagel et al., 2020; Li et al., 2021).
Language Generation.We begin our large-scale study by compressing the entire OPT and BLOOM
model families to 3- and 4-bit.  We then evaluate those models on several language tasks including
WikiText2 (Merity et al., 2016) (see Figure 1 as well as Tables 3 and 4), Penn Treebank (PTB) (Mar-
cus et al., 1994) and C4 (Raffel et al., 2020) (both in Appendix A.3). We focus on these perplexity-
based tasks, as they are known to be particularly sensitive to model quantization (Yao et al., 2022).
On OPT models, GPTQ clearly outperforms RTN, by significant margins. For example, GPTQ loses
only 0.03 perplexity at 4-bit on the 175B model, while RTN drops 2.2 points, performing worse than
the10×smaller full-precision 13B model. At 3-bit, RTN collapses completely, while GPTQ can still
maintain reasonable perplexity, in particular for larger models. BLOOM shows a similar pattern: the
gaps between methods are however usually a bit smaller, indicating that this model family might be
easier to quantize. One interesting trend (see also Figure 1) is that larger models generally (with the
exception of OPT-66B
## 2
) appear easier to quantize.  This is good news for practical applications, as
these are the cases where compression is also the most necessary.
OPTBits125M350M1.3B2.7B6.7B13B30B66B175B
full1627.6522.0014.6312.4710.8610.139.569.348.34
## RTN437.2825.9448.1716.9212.1011.3210.9811010.54
## GPTQ431.1224.2415.4712.8711.3910.319.639.558.37
RTN31.3e364.571.3e41.6e45.8e33.4e31.6e36.1e37.3e3
## GPTQ353.8533.7920.9716.8814.8611.6110.2714.168.68
Table 3: OPT perplexity results on WikiText2.
BLOOMBits560M1.1B1.7B3B7.1B176B
full1622.4217.6915.3913.4811.378.11
## RTN425.9022.0016.9714.7612.108.37
## GPTQ424.0319.0516.4814.2011.738.21
## RTN357.0850.1963.5939.3617.38571
## GPTQ332.3125.0821.1117.4013.478.64
Table 4: BLOOM perplexity results for WikiText2.
175 Billion Parameter Models.We now examine BLOOM-176B and OPT-175B, the largest dense
openly-available models. Table 5 summarizes results across Wikitext-2, PTB, C4. We observe that,
at 4 bits, GPTQ models reach only≤0.25lower perplexity than the full-precision versions, with a
large gap to RTN results on OPT-175B. At 3-bit, RTN collapses, while GPTQ is still able to maintain
good performance on most tasks, losing only0.3−0.6points for more than5×compression.  We
note that GPTQ’s accuracy can be further improved via finer-granularity grouping (Park et al., 2022):
group-size 1024 (≈0.02 extra bits) improves perplexities by about0.2on average and group-size
128 (≈0.15 extra bits) by another0.1, which is only0.1−0.3off from the uncompressed accuracy.
## 2
Upon closer inspection of the OPT-66B model, it appears that this is correlated with the fact that this trained
model has a significant fraction of dead units in the early layers, which may make it harder to compress.
## 7

Published as a conference paper at ICLR 2023
We note that grouping interacts very well with GPTQ, as the group parameters can be determined
during the quantization process of each layer, always using the most current updated weights.
MethodBits
## OPT-175BBLOOM-176B
Wiki2PTBC4LAMB.↑Wiki2PTBC4LAMB.↑
## Baseline168.3412.0110.1375.598.1114.5911.7167.40
## RTN410.5414.2211.6171.348.3715.0012.0466.70
## GPTQ48.3712.2610.2876.808.2114.7511.8167.71
RTN37.3e38.0e34.6e30571.107.598.0.17
## GPTQ38.6812.6810.6776.198.6415.5712.2765.10
GPTQ3/g10248.4512.4810.4777.398.3515.0111.9867.47
GPTQ3/g1288.4512.3710.3676.428.2614.8911.8567.86
Table 5:  Results summary for OPT-175B and BLOOM-176B. “g1024” and “g128” denote results
with groupings of size 1024 and 128, respectively.
Practical Speedups.Finally, we study practical applications.  As an interesting use-case, we focus
on the OPT-175B model:  quantized to 3 bits,  this model takes approximately 63GB of memory,
including the embeddings and the output layer, which are kept in full FP16 precision. Additionally,
storing the complete history of keys and values for all layers, a common optimization for generation
tasks,  consumes  another≈9GB  for  the  maximum  of  2048  tokens.   Hence,  we  can  actually  fit
the entire quantized model into a single 80GB A100 GPU, which can be executed by dynamically
dequantizing layers as they are required during inference (the model would not fully fit using 4
bits).  For reference, standard FP16 execution requires 5x80GB GPUs, and the state-of-the-art 8bit
LLM.int8() quantizer (Dettmers et al., 2022) requires 3 such GPUs.
Next, we consider language generation, one of the most appealing applications of these models, with
the goal of latency reduction.  Unlike LLM.int8(), which reduces memory costs but has the same
runtime as the FP16 baseline, we show that our quantized models can achieve significant speedups
for this application. For language generation, the model processes and outputs one token at-a-time,
which for OPT-175B can easily take a few 100s of milliseconds per token.  Increasing the speed at
which the user receives generated results is challenging, as compute is dominated by matrix-vector
products.  Unlike matrix-matrix products, these are primarily limited by memory bandwidth.  We
address this problem by developing a quantized-matrix full-precision-vector product kernel which
performs a matrix vector product by dynamically dequantizing weights when needed. Most notably,
this doesnotrequire any activation quantization.  While dequantization consumes extra compute,
the kernel has to access a lot less memory, leading to significant speedups, as shown in Table 6. We
note that almost all of the speedup is due to our kernels, as communication costs are negligible in
our standard HuggingFace-accelerate-like setting (see Appendix A.2.2 for details).
GPUFP163bitSpeedupGPU reduction
A6000 – 48GB589ms130ms4.53×8→2
A100 – 80GB230ms71ms3.24×5→1
Table 6: Average per-token latency (batch size 1) when generating sequences of length 128.
For example, using our kernels, the 3-bit OPT-175B model obtained via GPTQ running on a single
A100 is about3.25×faster than the FP16 version (running on 5 GPUs) in terms of average time per
token.  More accessible GPUs, such as the NVIDIA A6000, have much lower memory bandwidth,
so this strategy is even more effective:  executing the 3-bit OPT-175B model on 2x A6000 GPUs
reduces latency from 589 milliseconds for FP16 inference (on 8 GPUs) to 130 milliseconds, a4.5×
latency reduction.
Zero-Shot Tasks.While our focus is on language generation, we also evaluate the performance
of quantized models on some popular zero-shot tasks, namely LAMBADA (Paperno et al., 2016),
ARC (Easy and Challenge) (Boratko et al., 2018) and PIQA (Tata & Patel, 2003). Figure 3 visualizes
model performance on LAMBADA (and see also “Lamb.” results in Table 5).  We observe similar
behavior as before: the outliers are that 1) quantization appears “easier” across the whole spectrum
of models at 4-bit, where even RTN performs relatively well, and 2) at 3-bit, RTN breaks down,
while GPTQ still provides good accuracy. We provide additional results in Appendix A.4.
## 8

Published as a conference paper at ICLR 2023
## 10
## 1
## 10
## 0
## 10
## 1
## 10
## 2
#params in billions
## 0.0
## 0.2
## 0.4
## 0.6
## 0.8
Accuracy on LAMBADA
OPT Family
## 10
## 0
## 10
## 1
## 10
## 2
#params in billions
BLOOM Family
FP164bit GPTQ4bit RTN3bit GPTQ3bit RTN
Figure 3: The accuracy of OPT and BLOOM models post-GPTQ, measured on LAMBADA.
Additional Tricks.While our experiments so far have focused exclusively on vanilla row-wise
quantization, we want to emphasize that GPTQ iscompatible with essentially any choice of quanti-
zation grid.  For example, it is easily combined with standardgrouping(Alistarh et al., 2017; Park
et al., 2022), i.e. applying independent quantization to groups ofgconsecutive weights. As shown in
the last rows of Table 5, this can bring noticeable extra accuracy for the largest models at 3-bit. Fur-
ther, as visualized in Figure 4, it significantly reduces the accuracy losses for medium sized models
at 4-bit precision.
ModelFP16g128g64g323-bit
## OPT-175B8.349.589.188.948.68
## BLOOM8.119.559.178.838.64
Table  7:   2-bit  GPTQ  quantization  results  with
varying group-sizes; perplexity on WikiText2.
## 10
## 0
## 10
## 1
#params in billions
## 9
## 10
## 11
## 12
## 13
## 14
## 15
## 16
Perplexity on WikiText2
OPT Models 1.3B to 30B
## 4bit
## 4bit/g1024
## 4bit/g128
## FP16
Figure  4:GPTQ  at  4-bit  with  different
group-sizes on medium sized OPT models.
Extreme Quantization.Lastly, grouping also makes it possible to achieve reasonable performance
for extreme quantization,  to around 2-bits per component on average.   Table 7 shows results on
WikiText2  when  quantizing  the  biggest  models  to  2-bit  with  varying  group-sizes.   At≈2.2bit
(group-size 128; using FP16 scale and 2-bit zero point per group) the perplexity increase is already
less than 1.5 points, while dropping to 0.6 - 0.7 at≈2.6bit (group-size 32), which is only slightly
worse  than  vanilla  3-bit  and  might  be  interesting  for  practical  kernel  implementations.   Further,
if we reduce group size to 8, we can applyternary(-1, 0, +1) quantization, which achieves 9.20
WikiText2 PPL on OPT-175B, a less than 1 point drop.  While this leads to worse compression on
average relative to the 2-bit numbers above, this pattern could be efficiently implemented on custom
hardware such as FPGAs.  In summary, these results are an encouraging first step towards pushing
highly-accurateone-shotcompression of very large language models,  even lower than 3 bits per
value on average.
## 6SUMMARY ANDLIMITATIONS
We have presented GPTQ, an approximate second-order method for quantizing truly large language
models.  GPTQ can accurately compress some of the largest publicly-available models down to 3
and 4 bits, which leads to significant usability improvements, and to end-to-end speedups, at low
accuracy loss. We hope that our method will make these models accessible to more researchers and
practitioners.  At the same time, we emphasize some significant limitations:  On the technical side,
our method obtains speedups from reduced memory movement, and does not lead to computational
reductions.   In  addition,  our  study  focuses  on  generative  tasks,  and  does  not  consider  activation
quantization. These are natural directions for future work, and we believe this can be achieved with
carefully-designed GPU kernels and existing techniques (Yao et al., 2022; Wu et al., 2022).
## 9

Published as a conference paper at ICLR 2023
## ACKNOWLEDGMENTS
Elias Frantar and Dan Alistarh gratefully acknowledge funding from the European Research Coun-
cil (ERC) under the European Union’s Horizon 2020 programme (grant agreement No.   805223
ScaleML),  as  well  as  experimental  support  from  Eldar  Kurtic,  and  from  the  IST  Austria  IT  de-
partment, in particular Stefano Elefante, Andrei Hornoiu, and Alois Schloegl.  The work of Saleh
Ashkboos and Torsten Hoefler was supported by the PASC DaCeMI project, received EuroHPC-JU
funding under grant MAELSTROM, No.  955513.  We thank the Swiss National Supercomputing
Center (CSCS) for supporting us with compute infrastructure.
## 7ETHICSSTATEMENT
Our work introduces a general method for compressing large language models (LLMs) via quan-
tization,  with little-to-no accuracy loss in terms of standard accuracy metrics such as perplexity.
Our method is task-agnostic, as it only uses a tiny amount of randomly-chosen data for calibration.
We therefore do not foresee any significant ethical implications arising directly from the technical
details of our method.  However, one possible consideration is that our study focused on “leading
accuracy” metrics that are standard in the literature, such as perplexity, which is essentially standard
in the literature (Dettmers et al., 2022; Yao et al., 2022). We believe a thorough study of the impact
of compression upon secondary measures, and in particular bias effects (Bender et al., 2021) is war-
ranted, and may be rendered easier through our work. At the same time, our work makes inference
on extremely large language models more accessible, for better or for worse.  We believe that, in
time, such tools will become much easier to use and deploy, making the need to understand their
power and limitations even more stringent.
## 8REPRODUCIBILITYSTATEMENT
In the Supplementary Materials, we provide code to reproduce all experiments in this paper.  More
specifically, this includes:
-  Compressing all models from the OPT and BLOOM model families to 2/3/4 bits.
-  Evaluating perplexity of the quantized models.
-  Our 3-bit CUDA kernel together with compressed inference benchmarking features.
-  Code for the ZeroShot experiments.
-  A README file providing sample commands and information on how to run all scripts.
## REFERENCES
Dan Alistarh, Demjan Grubic, Jerry Li, Ryota Tomioka, and Milan Vojnovic.  QSGD: Randomized
quantization for communication-efficient stochastic gradient descent.  InConference on Neural
Information Processing Systems (NeurIPS), 2017.
Emily M Bender, Timnit Gebru, Angelina McMillan-Major, and Shmargaret Shmitchell.   On the
dangers of stochastic parrots:  Can language models be too big?   In2021 ACM Conference on
Fairness, Accountability, and Transparency, 2021.
Michael Boratko, Harshit Padigela, Divyendra Mikkilineni, Pritish Yuvraj, Rajarshi Das, Andrew
McCallum, Maria Chang, Achille Fokoue-Nkoutche, Pavan Kapanipathi, Nicholas Mattei, et al.
A systematic classification of knowledge, reasoning, and context within the ARC dataset.arXiv
preprint arXiv:1806.00358, 2018.
Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal,
Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al.  Language models are
few-shot learners. InConference on Neural Information Processing Systems (NeurIPS), 2020.
Tri Dao, Daniel Y Fu, Stefano Ermon, Atri Rudra, and Christopher R
## ́
e.  FlashAttention:  Fast and
memory-efficient exact attention with io-awareness.arXiv preprint arXiv:2205.14135, 2022.
## 10

Published as a conference paper at ICLR 2023
Tim  Dettmers,  Mike  Lewis,  Younes  Belkada,  and  Luke  Zettlemoyer.   LLM.int8():  8-bit  matrix
multiplication for transformers at scale.arXiv preprint arXiv:2208.07339, 2022.
Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.  BERT: Pre-training of deep
bidirectional transformers for language understanding. InNorth American Chapter of the Associ-
ation for Computational Linguistics (NAACL), 2019.
Elias  Frantar,  Eldar  Kurtic,  and  Dan  Alistarh.   M-FAC:  Efficient  matrix-free  approximations  of
second-order information.  InConference on Neural Information Processing Systems (NeurIPS),
## 2021.
Elias Frantar, Sidak Pal Singh, and Dan Alistarh. Optimal Brain Compression: A framework for ac-
curate post-training quantization and pruning.arXiv preprint arXiv:2208.11580, 2022. Accepted
to NeurIPS 2022, to appear.
Amir Gholami,  Sehoon Kim,  Zhen Dong,  Zhewei Yao,  Michael W Mahoney,  and Kurt Keutzer.
A  survey  of  quantization  methods  for  efficient  neural  network  inference.arXiv  preprint
arXiv:2103.13630, 2021.
Babak Hassibi, David G Stork, and Gregory J Wolff.  Optimal brain surgeon and general network
pruning. InIEEE International Conference on Neural Networks, 1993.
Torsten  Hoefler,  Dan  Alistarh,  Tal  Ben-Nun,  Nikoli  Dryden,  and  Alexandra  Peste.   Sparsity  in
deep learning: Pruning and growth for efficient inference and training in neural networks.arXiv
preprint arXiv:2102.00554, 2021.
Itay  Hubara,  Yury  Nahshan,  Yair  Hanani,  Ron  Banner,  and  Daniel  Soudry.Improving  post
training neural quantization:  Layer-wise calibration and integer programming.arXiv preprint
arXiv:2006.10518, 2020.
Itay Hubara,  Yury Nahshan,  Yair Hanani,  Ron Banner,  and Daniel Soudry.   Accurate post train-
ing quantization with small calibration sets.  InInternational Conference on Machine Learning
## (ICML), 2021.
Hugo Laurenc ̧on, Lucile Saulnier, Thomas Wang, Christopher Akiki, Albert Villanova del Moral,
## Teven Le Scao, Leandro Von Werra, Chenghao Mou, Eduardo Gonz
## ́
alez Ponferrada, Huu Nguyen,
et al. The BigScience corpus: A 1.6 TB composite multilingual dataset. 2022.
Yuhang Li, Ruihao Gong, Xu Tan, Yang Yang, Peng Hu, Qi Zhang, Fengwei Yu, Wei Wang, and
Shi Gu.   BRECQ: Pushing the limit of post-training quantization by block reconstruction.   In
International Conference on Learning Representations (ICLR), 2021.
Mitch Marcus, Grace Kim, Mary Ann Marcinkiewicz, Robert MacIntyre, Ann Bies, Mark Ferguson,
Karen Katz, and Britta Schasberger. The penn treebank: Annotating predicate argument structure.
InHuman Language Technology:  Proceedings of a Workshop held at Plainsboro, New Jersey,
## March 8-11, 1994, 1994.
Stephen Merity,  Caiming Xiong,  James Bradbury,  and Richard Socher.   Pointer sentinel mixture
models.arXiv preprint arXiv:1609.07843, 2016.
Markus Nagel, Rana Ali Amjad, Mart Van Baalen, Christos Louizos, and Tijmen Blankevoort. Up or
down? Adaptive rounding for post-training quantization. InInternational Conference on Machine
Learning (ICML), 2020.
Markus  Nagel,  Marios  Fournarakis,  Rana  Ali  Amjad,  Yelysei  Bondarenko,  Mart  van  Baalen,
and  Tijmen  Blankevoort.A  white  paper  on  neural  network  quantization.arXiv  preprint
arXiv:2106.08295, 2021.
Yury Nahshan, Brian Chmiel, Chaim Baskin, Evgenii Zheltonozhskii, Ron Banner, Alex M Bron-
stein, and Avi Mendelson.  Loss aware post-training quantization.Machine Learning, 110(11):
## 3245–3262, 2021.
## Denis Paperno,  Germ
## ́
an Kruszewski,  Angeliki Lazaridou,  Quan Ngoc Pham,  Raffaella Bernardi,
Sandro Pezzelle, Marco Baroni, Gemma Boleda, and Raquel Fern
## ́
andez. The LAMBADA dataset:
Word prediction requiring a broad discourse context.arXiv preprint arXiv:1606.06031, 2016.
## 11

Published as a conference paper at ICLR 2023
Gunho Park, Baeseong Park, Se Jung Kwon, Byeongwook Kim, Youngjoo Lee, and Dongsoo Lee.
nuQmm:  Quantized matmul for efficient inference of large-scale generative language models.
arXiv preprint arXiv:2206.09557, 2022.
Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor
Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, et al. Pytorch: An imperative style, high-
performance  deep  learning  library.   InConference  on  Neural  Information  Processing  Systems
(NeurIPS), 2019.
Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. Language
models are unsupervised multitask learners.OpenAI blog, 1(8):9, 2019.
Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi
Zhou, Wei Li, and Peter Liu.  Exploring the limits of transfer learning with a unified text-to-text
transformer.Journal of Machine Learning Research, 21(140):1–67, 2020.
Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, and Percy Liang.  SQuAD: 100,000+ questions
for machine comprehension of text.  InConference on Empirical Methods in Natural Language
Processing (EMNLP), 2016.
Sidak Pal Singh and Dan Alistarh.  WoodFisher:  Efficient second-order approximation for neural
network compression. InConference on Neural Information Processing Systems (NeurIPS), 2020.
Sandeep Tata and Jignesh M Patel. PiQA: An algebra for querying protein data sets. InInternational
Conference on Scientific and Statistical Database Management, 2003.
Ashish  Vaswani,  Noam  Shazeer,  Niki  Parmar,  Jakob  Uszkoreit,  Llion  Jones,  Aidan  N  Gomez,
Łukasz Kaiser,  and Illia Polosukhin.   Attention is all you need.   InConference on Neural In-
formation Processing Systems (NeurIPS), 2017.
Peisong Wang, Qiang Chen, Xiangyu He, and Jian Cheng.  Towards accurate post-training network
quantization via bit-split and stitching. InInternational Conference on Machine Learning (ICML),
## 2020.
Xiaoxia Wu, Zhewei Yao, Minjia Zhang, Conglong Li, and Yuxiong He.  Extreme compression for
pre-trained transformers made simple and efficient.arXiv preprint arXiv:2206.01859, 2022.
Zhewei Yao, Reza Yazdani Aminabadi, Minjia Zhang, Xiaoxia Wu, Conglong Li, and Yuxiong He.
ZeroQuant: Efficient and affordable post-training quantization for large-scale transformers.arXiv
preprint arXiv:2206.01861, 2022.
Susan Zhang, Stephen Roller, Naman Goyal, Mikel Artetxe, Moya Chen, Shuohui Chen, Christo-
pher Dewan,  Mona Diab,  Xian Li,  Xi Victoria Lin,  et al.   OPT: Open pre-trained transformer
language models.arXiv preprint arXiv:2205.01068, 2022.
Lianmin Zheng, Zhuohan Li, Hao Zhang, Yonghao Zhuang, Zhifeng Chen, Yanping Huang, Yida
Wang, Yuanzhong Xu, Danyang Zhuo, Joseph E Gonzalez, et al.   Alpa:  Automating inter-and
intra-operator parallelism for distributed deep learning.arXiv preprint arXiv:2201.12023, 2022.
## 12

Published as a conference paper at ICLR 2023
## AAPPENDIX
## A.1ADDITIONALCOMPARISON WITHOBQ
We now provide an additional comparison between GPTQ and OBQ on BERT-base/SQuAD Ra-
jpurkar et al. (2016) and OPT-125M/WikiText2, which is one of the largest models to which OBQ
can be reasonably applied.
## Method
BERT-baseOPT-125M
## 88.53 F1↑27.66 PPL↓
## 4bit3bit4bit3bit
## OBQ88.2385.2932.5269.32
## GPTQ88.1886.0231.1253.85
Table 8: Comparison of GPTQ relative to OBQ on BERT-base/SQuAD and OPT-125M/WikiText2.
## A.2EXPERIMENTDETAILS
This section provides additional details about our experiment setup, in particular regarding the model
evaluation and the setup of our timing experiments.
## A.2.1EVALUATION
For language generation experiments, we calculate the perplexity, in standard fashion like Radford
et  al.  (2019),  as  follows:  First,  the  entire  validation  set  is  concatenated  using  two  linebreaks  as
separators and encoded using the default HuggingFace tokenizer of each model. Next, the sequence
is split into non-overlapping segments of width 2048, the full context size of our models. These are
sent through the model to collect the log-probabilities corresponding to the next token each.  Their
exponentiated average is the final perplexity we report.
For zero-shot tasks we follow the EleutherAI evaluation harness
## 3
in terms of data preprocessing and
final score calculation.  We note that we evaluate all individual samples separately and thus do not
apply any padding.
## A.2.2TIMINGEXPERIMENTSETUP
Our timing experiments are performed following the standard HuggingFace/accelerate
## 4
setup also
used by the recent work LLM.int8() (Dettmers et al., 2022).  In this setting, the model is split by
distributing chunks of consecutive layers across GPUs. Importantly, in this setup the communication
costs are minimal,<5%of the total runtime even when working with 8 GPUs. This means almost
all of the reported speedups are due to our quantized-matrix full-precision vector product kernels.
We emphasize that the only difference between the FP16 baseline and our quantized models are the
kernels used to perform the underlying matrix-vector products.
This means all overheads due to HuggingFace, attention or non-quantized operations like residuals
or LayerNorms are exactly the same. Consequently, our quantized models should benefit from more
advanced distribution strategies (Zheng et al., 2022) or more efficient attention kernels (Dao et al.,
2022) just as much as our baseline.
In general, our kernels target generative inference in the low batch-size setting (for simplicity, we
consider  only  batchsize  1)  where  the  underlying  (close  to)  matrix-vector  products  are  memory-
bound.  For non-generative and large-batch applications, operations may be compute- rather than
memory-bound and our kernels thus not directly applicable. Instead, one could simply decompress
the matrix before performing the corresponding matrix-matrix calculations:  this takes<1.5ms on
an A100 and<3ms on an A6000 compared to 76ms/365ms for the subsequent OPT-175B FC2 layer
computation with batchsize16×1024tokens. Hence, for such applications our methods significantly
reduce the required number of GPUs at very little computational overhead. This is similar to recent
work (Dettmers et al., 2022), but we achieve a2.5×higher compression rate.
## 3
https://github.com/EleutherAI/lm-evaluation-harness
## 4
https://huggingface.co/docs/accelerate/index
## 13

Published as a conference paper at ICLR 2023
## A.3ADDITIONALLANGUAGEGENERATIONRESULTS
Tables 9, 10, 11 and 12 show additional results for language generation tasks.
OPTBits125M350M1.3B2.7B6.7B13B30B66B175B
full1638.9931.0820.2917.9715.7714.5214.0413.3612.01
## RTN453.8936.7957.3031.0518.8416.5115.40225.6614.22
## GPTQ445.1734.5221.8519.1416.5614.9414.2613.8112.26
RTN31.4e388.041.3e41.4e45.7e32.8e31.2e35.0e38.0e3
## GPTQ373.1947.0832.1024.8121.8816.6815.3628.1212.86
Table 9: OPT perplexity results on PTB.
BLOOMBits560M1.1B1.7B3B7.1B176B
full1643.6957.9630.0025.3420.8314.59
## RTN451.1066.8533.5827.6822.4215.00
## GPTQ446.9762.4731.8426.4921.6714.75
## RTN3126.185.106.66.7835.04107.
## GPTQ370.3587.0446.1134.0226.1415.57
Table 10: BLOOM perplexity results for PTB.
OPTBits125M350M1.3B2.7B6.7B13B30B66B175B
full1626.5622.5916.0714.3412.7112.0611.4410.9910.13
## RTN433.9126.2124.5118.4314.3613.3613.46309.11.61
## GPTQ429.2224.6316.9715.0013.1812.2611.5711.2310.28
RTN383455.495.2e31.1e45.3e33.1e31.4e33.5e34.6e3
## GPTQ342.4131.3321.6318.1717.1413.3412.2314.5910.67
Table 11: OPT perplexity results on C4. We note that the calibration data used by GPTQ is sampled
from the C4 training set, this task is thus not fully zero-shot.
BLOOMBits560M1.1B1.7B3B7.1B176B
full1626.6022.0519.4917.4915.2011.71
## RTN429.8924.4421.2618.7616.0612.04
## GPTQ428.0023.2520.5518.1015.6011.81
## RTN367.4960.71113.80.4922.59598.
## GPTQ335.7828.8325.3421.2517.6712.27
Table 12:  BLOOM perplexity results for C4.  We note that the calibration data used by GPTQ is
sampled from the C4 training set, this task is thus not fully zero-shot.
## 14

Published as a conference paper at ICLR 2023
## A.4ADDITIONALZEROSHOTRESULTS
This section contains additional results for zero-shot tasks.
OPTBits125M350M1.3B2.7B6.7B13B30B66B175B
full1639.1646.6758.8064.8268.7270.2372.3974.9375.59
## RTN418.3440.6236.3159.2764.6667.3870.4813.0871.34
## GPTQ434.7448.3856.4562.9766.3769.1272.4074.5076.80
## RTN30.1027.360.000.000.000.061.462.000.00
## GPTQ313.9332.3137.2652.2654.9864.1869.6957.0276.19
Table 13: OPT accuracy on LAMBADA.
BLOOMBits560M1.1B1.7B3B7.1B176B
full1634.0642.8546.7152.1257.7967.40
## RTN426.0039.0641.9245.8450.4866.70
## GPTQ431.7539.8046.2851.4154.6567.71
## RTN39.1015.9515.0224.5529.900.17
## GPTQ321.3128.7033.6543.1247.4165.10
Table 14: BLOOM accuracy on LAMBADA.
OPTBits125M350M1.3B2.7B6.7B13B30B66B175B
full1662.0264.7472.3674.8176.3976.8878.1879.7681.07
## RTN461.4363.4467.6373.7276.4476.0177.2660.0778.23
## GPTQ461.2663.7170.7373.9976.2876.6179.0079.3381.00
## RTN356.0960.6152.7751.9050.4952.9956.3750.8751.25
## GPTQ359.2561.3268.3471.3873.2975.2477.5871.2780.03
Table 15: OPT accuracy on PIQA.
BLOOMBits560M1.1B1.7B3B7.1B176B
full1665.0767.1469.9770.5173.7279.16
## RTN463.1165.2967.7469.8672.6979.00
## GPTQ464.3166.0568.7769.4272.9679.00
## RTN358.6060.8060.8866.2869.7053.32
## GPTQ361.6262.6265.1868.3470.9577.70
Table 16: BLOOM accuracy on PIQA.
OPTBits125M350M1.3B2.7B6.7B13B30B66B175B
full1639.6940.3650.9354.3460.1461.8365.4067.2671.04
## RTN436.3238.5549.2052.9057.6861.3161.1140.6663.93
## GPTQ439.0237.9259.9753.1159.7261.3265.1165.3568.69
## RTN330.4336.0727.9726.0525.0430.6034.2225.8426.77
## GPTQ336.1536.9146.1748.1953.4156.8259.7252.4465.36
Table 17: OPT accuracy on ARC-easy.
## 15

Published as a conference paper at ICLR 2023
BLOOMBits560M1.1B1.7B3B7.1B176B
full1641.7145.4148.1153.2457.3767.47
## RTN439.4042.5144.7051.3556.1466.33
## GPTQ440.2444.4944.4952.8256.1467.42
## RTN345.4446.8737.5845.0848.6128.87
## GPTQ339.1441.7942.8546.6351.5662.84
Table 18: BLOOM accuracy on ARC-easy.
OPTBits125M350M1.3B2.7B6.7B13B30B66B175B
full1622.8724.0629.4431.3134.5635.7538.1440.0243.94
## RTN422.4423.8124.9129.1832.5935.2435.4122.8737.71
## GPTQ422.9524.8328.2430.1233.7034.9037.8039.1642.75
## RTN321.7622.1823.5525.4325.8523.8119.9725.7723.81
## GPTQ322.5325.0927.6527.8231.9133.0235.8431.6641.04
Table 19: OPT accuracy on ARC-challenge.
BLOOMBits560M1.1B1.7B3B7.1B176B
full1624.1525.6826.7930.5533.4544.97
## RTN423.8923.3426.4529.5232.1743.17
## GPTQ423.4625.5125.9428.9232.2544.20
## RTN321.6722.8623.2927.1331.3124.74
## GPTQ323.2124.0624.9128.5830.9740.70
Table 20: BLOOM accuracy on ARC-challenge.
OPTBits125M350M1.3B2.7B6.7B13B30B66B175B
full1659.9663.2170.7871.7474.6076.6477.2877.3479.82
## RTN460.0263.0859.1370.7873.6574.4775.3751.2478.04
## GPTQ459.5863.4669.6470.4673.9076.1977.0877.1580.08
## RTN349.6556.7847.6146.9848.1249.2049.8448.1946.47
## GPTQ357.0360.1565.2568.4370.9773.0775.6871.2378.04
Table 21: OPT accuracy on StoryCloze.
BLOOMBits560M1.1B1.7B3B7.1B176B
full1661.9463.2765.4467.7971.9976.89
## RTN460.1560.6662.9567.0970.7276.00
## GPTQ461.1762.3264.4867.2271.3676.32
## RTN354.8756.0855.7959.8366.2048.50
## GPTQ357.8059.7761.8163.9769.2675.37
Table 22: BLOOM accuracy on StoryCloze.
## 16