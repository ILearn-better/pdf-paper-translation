<span  style="font-size: 17.21540069580078px;">Attention Is All You Need</span>

<span  style="font-size: 9.962599754333496px;">Ashish Vaswani</span><span  style="font-size: 9.962599754333496px;">Google Brain</span><span  style="font-size: 9.962599754333496px;">avaswani@google.com</span>
<span  style="font-size: 9.962599754333496px;">Noam Shazeer</span><span  style="font-size: 9.962599754333496px;">Google Brain</span><span  style="font-size: 9.962599754333496px;">noam@google.com</span>
<span  style="font-size: 9.962599754333496px;">Niki Parmar</span><span  style="font-size: 9.962599754333496px;">Google Research</span><span  style="font-size: 9.962599754333496px;">nikip@google.com</span>
<span  style="font-size: 9.962599754333496px;">Jakob Uszkoreit</span><span  style="font-size: 9.962599754333496px;">Google Research</span><span  style="font-size: 9.962599754333496px;">usz@google.com</span>
<span  style="font-size: 9.962599754333496px;">Llion Jones</span><span  style="font-size: 9.962599754333496px;">Google Research</span><span  style="font-size: 9.962599754333496px;">llion@google.com</span>
<span  style="font-size: 9.962599754333496px;">Aidan N. Gomez</span><span  style="font-size: 9.962599754333496px;">University of Toronto</span><span  style="font-size: 9.962599754333496px;">aidan@cs.toronto.edu</span>
<span  style="font-size: 9.962599754333496px;">Łukasz Kaiser</span><span  style="font-size: 9.962599754333496px;">Google Brain</span><span  style="font-size: 9.962599754333496px;">lukaszkaiser@google.com</span>
<span  style="font-size: 9.962599754333496px;">Illia Polosukhin</span><span  style="font-size: 9.962599754333496px;">illia.polosukhin@gmail.com</span>
<span  style="font-size: 11.9552001953125px;">Abstract</span>

<span  style="font-size: 10.061732292175293px;">The dominant sequence transduction models are based on complex recurrent or</span>
<span  style="font-size: 10.061732292175293px;">convolutional neural networks that include an encoder and a decoder. The best</span>
<span  style="font-size: 10.061732292175293px;">performing models also connect the encoder and decoder through an attention</span>
<span  style="font-size: 10.061732292175293px;">mechanism. We propose a new simple network architecture, the Transformer,</span>
<span  style="font-size: 10.061732292175293px;">entirely. Experiments on two machine translation tasks show these models to</span>
<span  style="font-size: 10.022196769714355px;">be superior in quality while being more parallelizable and requiring signiﬁcantly</span>
<span  style="font-size: 10.061732292175293px;">less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-</span>
<span  style="font-size: 10.061732292175293px;">to-German translation task, improving over the existing best results, including</span>
<span  style="font-size: 10.061732292175293px;">training for 3.5 days on eight GPUs, a small fraction of the training costs of the</span>
<span  style="font-size: 10.037040710449219px;">other tasks by applying it successfully to English constituency parsing both with</span>
<span  style="font-size: 9.962599754333496px;">large and limited training data.</span>
<span  style="font-size: 11.9552001953125px;">1</span>
<span  style="font-size: 11.9552001953125px;">Introduction</span>

<span  style="font-size: 10.061732292175293px;">Recurrent neural networks, long short-term memory [</span>
<span  style="font-size: 9.962599754333496px;">13</span><span  style="font-size: 10.061732292175293px;">] and gated recurrent [</span>
<span  style="font-size: 9.962599754333496px;">7</span><span  style="font-size: 10.061732292175293px;">] neural networks</span>
<span  style="font-size: 10.046924591064453px;">in particular, have been ﬁrmly established as state of the art approaches in sequence modeling and</span>



<span  style="font-size: 20.0px;">arXiv:1706.03762v5  [cs.CL]  6 Dec 2017</span>

<span  style="font-size: 10.061732292175293px;">transduction problems such as language modeling and machine translation [</span>
<span  style="font-size: 9.962599754333496px;">35</span><span  style="font-size: 10.061732292175293px;">,</span>
<span  style="font-size: 9.962599754333496px;"> 2</span><span  style="font-size: 10.061732292175293px;">,</span>
<span  style="font-size: 9.962599754333496px;"> 5</span><span  style="font-size: 10.061732292175293px;">]. Numerous</span>
<span  style="font-size: 9.962599754333496px;">architectures [38, 24, 15].</span>
<span  style="font-size: 10.061732292175293px;">Recurrent models typically factor computation along the symbol positions of the input and output</span>
<span  style="font-size: 9.982504844665527px;">sequences. Aligning the positions to steps in computation time, they generate a sequence of hidden</span>
<span  style="font-size: 9.962599754333496px;"> h</span><span  style="font-size: 9.962599754333496px;"> h</span><span  style="font-size: 9.962599754333496px;"> t</span><span  style="font-size: 9.962599754333496px;">21</span><span  style="font-size: 10.051863670349121px;">computation [</span>
<span  style="font-size: 9.962599754333496px;">32</span><span  style="font-size: 10.051863670349121px;">], while also improving model performance in case of the latter. The fundamental</span>
<span  style="font-size: 9.962599754333496px;">constraint of sequential computation, however, remains.</span>
<span  style="font-size: 9.982504844665527px;">tion models in various tasks, allowing modeling of dependencies without regard to their distance in</span>
<span  style="font-size: 9.962599754333496px;">2</span><span  style="font-size: 9.962599754333496px;"> 19</span><span  style="font-size: 9.962599754333496px;">27</span><span  style="font-size: 9.962599754333496px;">are used in conjunction with a recurrent network.</span>
<span  style="font-size: 10.061732292175293px;">In this work we propose the Transformer, a model architecture eschewing recurrence and instead</span>
<span  style="font-size: 10.032095909118652px;">relying entirely on an attention mechanism to draw global dependencies between input and output.</span>
<span  style="font-size: 9.962599754333496px;">The Transformer allows for signiﬁcantly more parallelization and can reach a new state of the art in</span><span  style="font-size: 9.962599754333496px;">translation quality after being trained for as little as twelve hours on eight P100 GPUs.</span>
<span  style="font-size: 11.9552001953125px;">2</span>
<span  style="font-size: 11.9552001953125px;">Background</span>

<span  style="font-size: 9.962599754333496px;">16</span><span  style="font-size: 9.962599754333496px;">18</span><span  style="font-size: 9.962599754333496px;">9</span><span  style="font-size: 10.061732292175293px;">it more difﬁcult to learn dependencies between distant positions [</span>
<span  style="font-size: 9.962599754333496px;">12</span><span  style="font-size: 10.061732292175293px;">]. In the Transformer this is</span>
<span  style="font-size: 10.061732292175293px;">reduced to a constant number of operations, albeit at the cost of reduced effective resolution due</span>
<span  style="font-size: 10.061732292175293px;">to averaging attention-weighted positions, an effect we counteract with Multi-Head Attention as</span>
<span  style="font-size: 9.962599754333496px;">described in section 3.2.</span>
<span  style="font-size: 10.061732292175293px;">of a single sequence in order to compute a representation of the sequence. Self-attention has been</span>
<span  style="font-size: 9.962599754333496px;">textual entailment and learning task-independent sentence representations [4, 27, 28, 22].</span>
<span  style="font-size: 10.061732292175293px;">End-to-end memory networks are based on a recurrent attention mechanism instead of sequence-</span>
<span  style="font-size: 9.962599754333496px;">language modeling tasks [34].</span>
<span  style="font-size: 10.061732292175293px;">To the best of our knowledge, however, the Transformer is the ﬁrst transduction model relying</span>
<span  style="font-size: 9.962599754333496px;">entirely on self-attention to compute representations of its input and output without using sequence-</span><span  style="font-size: 9.962599754333496px;">self-attention and discuss its advantages over models such as [17, 18] and [9].</span>
<span  style="font-size: 11.9552001953125px;">3</span>
<span  style="font-size: 11.9552001953125px;">Model Architecture</span>

<span  style="font-size: 9.962599754333496px;">5</span><span  style="font-size: 9.962599754333496px;"> 2</span><span  style="font-size: 9.962599754333496px;"> 35</span><span  style="font-size: 10.061732292175293px;">Here, the encoder maps an input sequence of symbol representations</span>
<span  style="font-size: 9.962599754333496px;"> (</span><span  style="font-size: 9.962599754333496px;">x</span><span  style="font-size: 9.962599754333496px;">, ..., x</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 10.061732292175293px;"> to a sequence</span>
<span  style="font-size: 10.061732292175293px;">of continuous representations</span>
<span  style="font-size: 9.962599754333496px;"> z</span><span  style="font-size: 9.962599754333496px;"> = (</span><span  style="font-size: 9.962599754333496px;">z</span><span  style="font-size: 9.962599754333496px;">, ..., z</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 10.061732292175293px;">. Given</span>
<span  style="font-size: 9.962599754333496px;"> z</span><span  style="font-size: 10.061732292175293px;">, the decoder then generates an output</span>
<span  style="font-size: 10.061732292175293px;">sequence</span>
<span  style="font-size: 9.962599754333496px;"> (</span><span  style="font-size: 9.962599754333496px;">y</span><span  style="font-size: 9.962599754333496px;">, ..., y</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 10.061732292175293px;"> of symbols one element at a time. At each step the model is auto-regressive</span>
<span  style="font-size: 9.962599754333496px;">[10], consuming the previously generated symbols as additional input when generating the next.</span>
<span  style="font-size: 10.022196769714355px;">The Transformer follows this overall architecture using stacked self-attention and point-wise, fully</span>
<span  style="font-size: 10.061732292175293px;">connected layers for both the encoder and decoder, shown in the left and right halves of Figure 1,</span>
<span  style="font-size: 9.962599754333496px;">respectively.</span>
<span  style="font-size: 9.962599754333496px;">2</span>

<span  style="font-size: 9.962599754333496px;">Figure 1: The Transformer - model architecture.</span>
<span  style="font-size: 9.962599754333496px;">3.1</span><span  style="font-size: 9.962599754333496px;">Encoder and Decoder Stacks</span>
<span  style="font-size: 9.962599754333496px;">Encoder:</span><span  style="font-size: 10.061732292175293px;">The encoder is composed of a stack of</span>
<span  style="font-size: 9.962599754333496px;"> N</span><span  style="font-size: 9.962599754333496px;"> = 6</span><span  style="font-size: 10.061732292175293px;"> identical layers. Each layer has two</span>
<span  style="font-size: 10.007330894470215px;">sub-layers. The ﬁrst is a multi-head self-attention mechanism, and the second is a simple, position-</span>
<span  style="font-size: 10.041984558105469px;">wise fully connected feed-forward network. We employ a residual connection [</span>
<span  style="font-size: 9.962599754333496px;">11</span><span  style="font-size: 10.041984558105469px;">] around each of</span>
<span  style="font-size: 10.061732292175293px;">the two sub-layers, followed by layer normalization [</span>
<span  style="font-size: 9.962599754333496px;">1</span><span  style="font-size: 10.061732292175293px;">]. That is, the output of each sub-layer is</span>
<span  style="font-size: 9.962599754333496px;">LayerNorm(</span><span  style="font-size: 9.962599754333496px;">x</span><span  style="font-size: 9.962599754333496px;"> + Sublayer(</span><span  style="font-size: 9.962599754333496px;">x</span><span  style="font-size: 9.962599754333496px;">))</span><span  style="font-size: 10.061732292175293px;">, where</span>
<span  style="font-size: 9.962599754333496px;"> Sublayer(</span><span  style="font-size: 9.962599754333496px;">x</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 10.061732292175293px;"> is the function implemented by the sub-layer</span>
<span  style="font-size: 9.962599754333496px;">itself. To facilitate these residual connections, all sub-layers in the model, as well as the embedding</span><span  style="font-size: 9.962599754333496px;">layers, produce outputs of dimension</span><span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.962599754333496px;"> = 512</span><span  style="font-size: 9.962599754333496px;">.</span>
<span  style="font-size: 9.962599754333496px;">Decoder:</span><span  style="font-size: 9.962599754333496px;"> N</span><span  style="font-size: 9.962599754333496px;"> = 6</span><span  style="font-size: 10.061732292175293px;">sub-layers in each encoder layer, the decoder inserts a third sub-layer, which performs multi-head</span>
<span  style="font-size: 10.061732292175293px;">around each of the sub-layers, followed by layer normalization. We also modify the self-attention</span>
<span  style="font-size: 10.061732292175293px;">sub-layer in the decoder stack to prevent positions from attending to subsequent positions. This</span>
<span  style="font-size: 9.962599754333496px;">predictions for position</span><span  style="font-size: 9.962599754333496px;"> i</span><span  style="font-size: 9.962599754333496px;"> can depend only on the known outputs at positions less than</span><span  style="font-size: 9.962599754333496px;"> i</span><span  style="font-size: 9.962599754333496px;">.</span>
<span  style="font-size: 9.962599754333496px;">3.2</span><span  style="font-size: 9.962599754333496px;">Attention</span>
<span  style="font-size: 9.962599754333496px;">query with the corresponding key.</span>
<span  style="font-size: 9.962599754333496px;">3</span>
<span  style="font-size: 9.962599754333496px;">Scaled Dot-Product Attention</span>

<span  style="font-size: 9.962599754333496px;">Multi-Head Attention</span>

<span  style="font-size: 10.061732292175293px;">Figure 2: (left) Scaled Dot-Product Attention. (right) Multi-Head Attention consists of several</span>
<span  style="font-size: 9.962599754333496px;">attention layers running in parallel.</span>
<span  style="font-size: 9.962599754333496px;">3.2.1</span><span  style="font-size: 9.962599754333496px;">Scaled Dot-Product Attention</span>
<span  style="font-size: 10.061732292175293px;">We call our particular attention "Scaled Dot-Product Attention" (Figure 2). The input consists of</span>
<span  style="font-size: 9.972557067871094px;">queries and keys of dimension</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.972557067871094px;">, and values of dimension</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.972557067871094px;">. We compute the dot products of the</span>
<span  style="font-size: 9.997407913208008px;">query with all keys, divide each by</span>
<span  style="font-size: 9.962599754333496px;"> </span><span  style="font-size: 9.962599754333496px;">√</span><span  style="font-size: 9.962599754333496px;">d</span><span  style="font-size: 9.997407913208008px;">, and apply a softmax function to obtain the weights on the</span>
<span  style="font-size: 9.962599754333496px;">values.</span>
<span  style="font-size: 10.061732292175293px;">In practice, we compute the attention function on a set of queries simultaneously, packed together</span>
<span  style="font-size: 9.977532386779785px;">into a matrix</span>
<span  style="font-size: 9.962599754333496px;"> Q</span><span  style="font-size: 9.977532386779785px;">. The keys and values are also packed together into matrices</span>
<span  style="font-size: 9.962599754333496px;"> K</span><span  style="font-size: 9.977532386779785px;"> and</span>
<span  style="font-size: 9.962599754333496px;"> V</span><span  style="font-size: 9.977532386779785px;"> . We compute</span>
<span  style="font-size: 9.962599754333496px;">the matrix of outputs as:</span>
<span  style="font-size: 9.962599754333496px;">Attention(</span><span  style="font-size: 9.962599754333496px;">Q, K, V</span><span  style="font-size: 9.962599754333496px;"> ) = softmax(</span><span  style="font-size: 9.962599754333496px;">QK</span>
<span  style="font-size: 9.962599754333496px;">√</span><span  style="font-size: 9.962599754333496px;">d</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 9.962599754333496px;">V</span><span  style="font-size: 9.962599754333496px;">(1)</span>
<span  style="font-size: 9.987475395202637px;">The two most commonly used attention functions are additive attention [</span>
<span  style="font-size: 9.962599754333496px;">2</span><span  style="font-size: 9.987475395202637px;">], and dot-product (multi-</span>
<span  style="font-size: 9.972557067871094px;">plicative) attention. Dot-product attention is identical to our algorithm, except for the scaling factor</span>
<span  style="font-size: 10.007330894470215px;">of</span>
<span  style="font-size: 10.007330894470215px;"> . Additive attention computes the compatibility function using a feed-forward network with</span>
<span  style="font-size: 10.061732292175293px;">a single hidden layer. While the two are similar in theoretical complexity, dot-product attention is</span>
<span  style="font-size: 9.962599754333496px;">matrix multiplication code.</span>
<span  style="font-size: 9.992443084716797px;">While for small values of</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.992443084716797px;"> the two mechanisms perform similarly, additive attention outperforms</span>
<span  style="font-size: 9.987475395202637px;">dot product attention without scaling for larger values of</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.987475395202637px;"> [</span>
<span  style="font-size: 9.962599754333496px;">3</span><span  style="font-size: 9.987475395202637px;">]. We suspect that for large values of</span>
<span  style="font-size: 9.962599754333496px;">d</span><span  style="font-size: 9.962599754333496px;">extremely small gradients</span><span  style="font-size: 9.962599754333496px;">. To counteract this effect, we scale the dot products by</span><span  style="font-size: 9.962599754333496px;"> .</span>
<span  style="font-size: 9.962599754333496px;">3.2.2</span><span  style="font-size: 9.962599754333496px;">Multi-Head Attention</span>
<span  style="font-size: 10.037040710449219px;">Instead of performing a single attention function with</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 10.037040710449219px;">-dimensional keys, values and queries,</span>
<span  style="font-size: 9.962599754333496px;"> h</span><span  style="font-size: 9.982504844665527px;">linear projections to</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.982504844665527px;">,</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.982504844665527px;"> and</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.982504844665527px;"> dimensions, respectively. On each of these projected versions of</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 10.061732292175293px;">output values. These are concatenated and once again projected, resulting in the ﬁnal values, as</span>
<span  style="font-size: 9.962599754333496px;">depicted in Figure 2.</span>

<span  style="font-size: 9.962599754333496px;">4</span>
<span  style="font-size: 9.982504844665527px;">Multi-head attention allows the model to jointly attend to information from different representation</span>
<span  style="font-size: 9.962599754333496px;">subspaces at different positions. With a single attention head, averaging inhibits this.</span>
<span  style="font-size: 9.962599754333496px;">MultiHead(</span><span  style="font-size: 9.962599754333496px;">Q, K, V</span><span  style="font-size: 9.962599754333496px;"> ) = Concat(head</span><span  style="font-size: 9.962599754333496px;">, ...,</span><span  style="font-size: 9.962599754333496px;"> head</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 9.962599754333496px;">W</span>
<span  style="font-size: 9.962599754333496px;">where</span><span  style="font-size: 9.962599754333496px;"> head</span><span  style="font-size: 9.962599754333496px;"> = Attention(</span><span  style="font-size: 9.962599754333496px;">QW</span><span  style="font-size: 9.962599754333496px;"> </span><span  style="font-size: 9.962599754333496px;">, KW</span><span  style="font-size: 9.962599754333496px;"> </span><span  style="font-size: 9.962599754333496px;">, V W</span><span  style="font-size: 9.962599754333496px;"> </span><span  style="font-size: 9.962599754333496px;">)</span>
<span  style="font-size: 9.962599754333496px;"> W</span><span  style="font-size: 9.962599754333496px;">∈</span><span  style="font-size: 9.962599754333496px;"> R</span><span  style="font-size: 9.962599754333496px;"> W</span><span  style="font-size: 9.962599754333496px;">∈</span><span  style="font-size: 9.962599754333496px;"> R</span><span  style="font-size: 9.962599754333496px;"> W</span><span  style="font-size: 9.962599754333496px;">∈</span><span  style="font-size: 9.962599754333496px;"> R</span><span  style="font-size: 9.962599754333496px;">and</span><span  style="font-size: 9.962599754333496px;"> W</span><span  style="font-size: 9.962599754333496px;"> </span><span  style="font-size: 9.962599754333496px;">∈</span><span  style="font-size: 9.962599754333496px;"> R</span><span  style="font-size: 9.962599754333496px;">.</span>
<span  style="font-size: 10.061732292175293px;">In this work we employ</span>
<span  style="font-size: 9.962599754333496px;"> h</span><span  style="font-size: 9.962599754333496px;"> = 8</span><span  style="font-size: 10.061732292175293px;"> parallel attention layers, or heads. For each of these we use</span>
<span  style="font-size: 9.962599754333496px;">d</span><span  style="font-size: 9.962599754333496px;"> =</span><span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.962599754333496px;"> =</span><span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.962599754333496px;">/h</span><span  style="font-size: 9.962599754333496px;"> = 64</span><span  style="font-size: 9.962599754333496px;">is similar to that of single-head attention with full dimensionality.</span>
<span  style="font-size: 9.962599754333496px;">3.2.3</span><span  style="font-size: 9.962599754333496px;">Applications of Attention in our Model</span>
<span  style="font-size: 9.962599754333496px;">The Transformer uses multi-head attention in three different ways:</span>
<span  style="font-size: 9.962599754333496px;">•</span><span  style="font-size: 10.061732292175293px;"> In "encoder-decoder attention" layers, the queries come from the previous decoder layer,</span>
<span  style="font-size: 10.061732292175293px;">and the memory keys and values come from the output of the encoder. This allows every</span>
<span  style="font-size: 10.032095909118652px;">position in the decoder to attend over all positions in the input sequence. This mimics the</span>
<span  style="font-size: 10.061732292175293px;">typical encoder-decoder attention mechanisms in sequence-to-sequence models such as</span>
<span  style="font-size: 9.962599754333496px;">[38, 2, 9].</span>
<span  style="font-size: 9.962599754333496px;">•</span><span  style="font-size: 10.061732292175293px;"> The encoder contains self-attention layers. In a self-attention layer all of the keys, values</span>
<span  style="font-size: 10.022196769714355px;">and queries come from the same place, in this case, the output of the previous layer in the</span>
<span  style="font-size: 9.962599754333496px;">encoder.</span>
<span  style="font-size: 9.962599754333496px;">•</span><span  style="font-size: 10.012289047241211px;">all positions in the decoder up to and including that position. We need to prevent leftward</span>
<span  style="font-size: 9.962599754333496px;"> −∞</span><span  style="font-size: 9.962599754333496px;">of the softmax which correspond to illegal connections. See Figure 2.</span>
<span  style="font-size: 9.962599754333496px;">3.3</span><span  style="font-size: 9.962599754333496px;">Position-wise Feed-Forward Networks</span>
<span  style="font-size: 10.061732292175293px;">In addition to attention sub-layers, each of the layers in our encoder and decoder contains a fully</span>
<span  style="font-size: 10.007330894470215px;">connected feed-forward network, which is applied to each position separately and identically. This</span>
<span  style="font-size: 9.962599754333496px;">consists of two linear transformations with a ReLU activation in between.</span>
<span  style="font-size: 9.962599754333496px;">FFN(</span><span  style="font-size: 9.962599754333496px;">x</span><span  style="font-size: 9.962599754333496px;">) = max(0</span><span  style="font-size: 9.962599754333496px;">, xW</span><span  style="font-size: 9.962599754333496px;"> +</span><span  style="font-size: 9.962599754333496px;"> b</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 9.962599754333496px;">W</span><span  style="font-size: 9.962599754333496px;"> +</span><span  style="font-size: 9.962599754333496px;"> b</span><span  style="font-size: 9.962599754333496px;">(2)</span>
<span  style="font-size: 10.061732292175293px;">from layer to layer. Another way of describing this is as two convolutions with kernel size 1.</span>
<span  style="font-size: 10.061732292175293px;">The dimensionality of input and output is</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.962599754333496px;"> = 512</span><span  style="font-size: 10.061732292175293px;">, and the inner-layer has dimensionality</span>
<span  style="font-size: 9.962599754333496px;">d</span><span  style="font-size: 9.962599754333496px;"> = 2048</span><span  style="font-size: 9.962599754333496px;">.</span>
<span  style="font-size: 9.962599754333496px;">3.4</span><span  style="font-size: 9.962599754333496px;">Embeddings and Softmax</span>
<span  style="font-size: 10.061732292175293px;">Similarly to other sequence transduction models, we use learned embeddings to convert the input</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.982504844665527px;">mation and softmax function to convert the decoder output to predicted next-token probabilities. In</span>
<span  style="font-size: 9.962599754333496px;">30</span><span  style="font-size: 9.962599754333496px;"> </span><span  style="font-size: 9.962599754333496px;">√</span><span  style="font-size: 9.962599754333496px;">d</span>
<span  style="font-size: 9.962599754333496px;">3.5</span><span  style="font-size: 9.962599754333496px;">Positional Encoding</span>

<span  style="font-size: 9.962599754333496px;">5</span>
<span  style="font-size: 9.987475395202637px;">for different layer types.</span>
<span  style="font-size: 9.962599754333496px;"> n</span><span  style="font-size: 9.987475395202637px;"> is the sequence length,</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.987475395202637px;"> is the representation dimension,</span>
<span  style="font-size: 9.962599754333496px;"> k</span><span  style="font-size: 9.987475395202637px;"> is the kernel</span>
<span  style="font-size: 9.962599754333496px;">size of convolutions and</span><span  style="font-size: 9.962599754333496px;"> r</span><span  style="font-size: 9.962599754333496px;"> the size of the neighborhood in restricted self-attention.</span>
<span  style="font-size: 9.962599754333496px;">Layer Type</span><span  style="font-size: 9.962599754333496px;">Complexity per Layer</span><span  style="font-size: 9.962599754333496px;">Sequential</span><span  style="font-size: 9.962599754333496px;">Maximum Path Length</span><span  style="font-size: 9.962599754333496px;">Operations</span>
<span  style="font-size: 9.962599754333496px;">Self-Attention</span><span  style="font-size: 9.962599754333496px;">O</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">n</span><span  style="font-size: 9.962599754333496px;"> </span><span  style="font-size: 9.962599754333496px;">·</span><span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 9.962599754333496px;">O</span><span  style="font-size: 9.962599754333496px;">(1)</span><span  style="font-size: 9.962599754333496px;">O</span><span  style="font-size: 9.962599754333496px;">(1)</span><span  style="font-size: 9.962599754333496px;">Recurrent</span><span  style="font-size: 9.962599754333496px;">O</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">n</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 9.962599754333496px;">O</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">n</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 9.962599754333496px;">O</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">n</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 9.962599754333496px;">Convolutional</span><span  style="font-size: 9.962599754333496px;">O</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">k</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> n</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 9.962599754333496px;">O</span><span  style="font-size: 9.962599754333496px;">(1)</span><span  style="font-size: 9.962599754333496px;">O</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">log</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">n</span><span  style="font-size: 9.962599754333496px;">))</span><span  style="font-size: 9.962599754333496px;">Self-Attention (restricted)</span><span  style="font-size: 9.962599754333496px;">O</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">r</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> n</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 9.962599754333496px;">O</span><span  style="font-size: 9.962599754333496px;">(1)</span><span  style="font-size: 9.962599754333496px;">O</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">n/r</span><span  style="font-size: 9.962599754333496px;">)</span>
<span  style="font-size: 10.061732292175293px;">tokens in the sequence. To this end, we add "positional encodings" to the input embeddings at the</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.962599754333496px;">learned and ﬁxed [9].</span>
<span  style="font-size: 9.962599754333496px;">In this work, we use sine and cosine functions of different frequencies:</span>
<span  style="font-size: 9.962599754333496px;">PE</span><span  style="font-size: 9.962599754333496px;"> =</span><span  style="font-size: 9.962599754333496px;"> sin</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">pos/</span><span  style="font-size: 9.962599754333496px;">10000</span><span  style="font-size: 9.962599754333496px;">)</span>
<span  style="font-size: 9.962599754333496px;">PE</span><span  style="font-size: 9.962599754333496px;"> =</span><span  style="font-size: 9.962599754333496px;"> cos</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">pos/</span><span  style="font-size: 9.962599754333496px;">10000</span><span  style="font-size: 9.962599754333496px;">)</span>
<span  style="font-size: 9.962599754333496px;"> pos</span><span  style="font-size: 9.962599754333496px;"> i</span><span  style="font-size: 9.962599754333496px;"> 2</span><span  style="font-size: 9.962599754333496px;">π</span><span  style="font-size: 9.962599754333496px;"> 10000</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 2</span><span  style="font-size: 9.962599754333496px;">π</span><span  style="font-size: 10.061732292175293px;">chose this function because we hypothesized it would allow the model to easily learn to attend by</span>
<span  style="font-size: 10.061732292175293px;">relative positions, since for any ﬁxed offset</span>
<span  style="font-size: 9.962599754333496px;"> k</span><span  style="font-size: 10.061732292175293px;">,</span>
<span  style="font-size: 9.962599754333496px;"> PE</span><span  style="font-size: 10.061732292175293px;"> can be represented as a linear function of</span>
<span  style="font-size: 9.962599754333496px;">PE</span><span  style="font-size: 9.962599754333496px;">.</span>
<span  style="font-size: 9.96757984161377px;">We also experimented with using learned positional embeddings [</span>
<span  style="font-size: 9.962599754333496px;">9</span><span  style="font-size: 9.96757984161377px;">] instead, and found that the two</span>
<span  style="font-size: 10.061732292175293px;">versions produced nearly identical results (see Table 3 row (E)). We chose the sinusoidal version</span>
<span  style="font-size: 9.962599754333496px;">during training.</span>
<span  style="font-size: 11.9552001953125px;">4</span>
<span  style="font-size: 11.9552001953125px;">Why Self-Attention</span>

<span  style="font-size: 10.061732292175293px;">In this section we compare various aspects of self-attention layers to the recurrent and convolu-</span>
<span  style="font-size: 10.041984558105469px;">tional layers commonly used for mapping one variable-length sequence of symbol representations</span>
<span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">x</span><span  style="font-size: 9.962599754333496px;">, ..., x</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 10.061732292175293px;"> to another sequence of equal length</span>
<span  style="font-size: 9.962599754333496px;"> (</span><span  style="font-size: 9.962599754333496px;">z</span><span  style="font-size: 9.962599754333496px;">, ..., z</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 10.061732292175293px;">, with</span>
<span  style="font-size: 9.962599754333496px;"> x</span><span  style="font-size: 9.962599754333496px;">, z</span><span  style="font-size: 9.962599754333496px;"> ∈</span><span  style="font-size: 9.962599754333496px;"> R</span><span  style="font-size: 10.061732292175293px;">, such as a hidden</span>
<span  style="font-size: 9.962599754333496px;">consider three desiderata.</span>
<span  style="font-size: 9.96757984161377px;">One is the total computational complexity per layer. Another is the amount of computation that can</span>
<span  style="font-size: 9.962599754333496px;">be parallelized, as measured by the minimum number of sequential operations required.</span>
<span  style="font-size: 10.017244338989258px;">The third is the path length between long-range dependencies in the network. Learning long-range</span>
<span  style="font-size: 10.022196769714355px;">dependencies is a key challenge in many sequence transduction tasks. One key factor affecting the</span>
<span  style="font-size: 10.061732292175293px;">ability to learn such dependencies is the length of the paths forward and backward signals have to</span>
<span  style="font-size: 10.037040710449219px;">traverse in the network. The shorter these paths between any combination of positions in the input</span>
<span  style="font-size: 9.962599754333496px;">12</span><span  style="font-size: 9.96757984161377px;">the maximum path length between any two input and output positions in networks composed of the</span>
<span  style="font-size: 9.962599754333496px;">different layer types.</span>
<span  style="font-size: 10.061732292175293px;">executed operations, whereas a recurrent layer requires</span>
<span  style="font-size: 9.962599754333496px;"> O</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">n</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 10.061732292175293px;"> sequential operations. In terms of</span>
<span  style="font-size: 10.061732292175293px;">computational complexity, self-attention layers are faster than recurrent layers when the sequence</span>
<span  style="font-size: 10.061732292175293px;">length</span>
<span  style="font-size: 9.962599754333496px;"> n</span><span  style="font-size: 10.061732292175293px;"> is smaller than the representation dimensionality</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 10.061732292175293px;">, which is most often the case with</span>
<span  style="font-size: 9.992443084716797px;">[</span>
<span  style="font-size: 9.962599754333496px;">38</span><span  style="font-size: 9.992443084716797px;">] and byte-pair [</span>
<span  style="font-size: 9.962599754333496px;">31</span><span  style="font-size: 9.992443084716797px;">] representations. To improve computational performance for tasks involving</span>
<span  style="font-size: 9.962599754333496px;"> r</span>
<span  style="font-size: 9.962599754333496px;">6</span>
<span  style="font-size: 9.962599754333496px;">path length to</span><span  style="font-size: 9.962599754333496px;"> O</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">n/r</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 9.962599754333496px;">. We plan to investigate this approach further in future work.</span>
<span  style="font-size: 9.987475395202637px;">A single convolutional layer with kernel width</span>
<span  style="font-size: 9.962599754333496px;"> k < n</span><span  style="font-size: 9.987475395202637px;"> does not connect all pairs of input and output</span>
<span  style="font-size: 9.962599754333496px;"> O</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">n/k</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 10.061732292175293px;">or</span>
<span  style="font-size: 9.962599754333496px;"> O</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">log</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">n</span><span  style="font-size: 9.962599754333496px;">))</span><span  style="font-size: 10.061732292175293px;"> in the case of dilated convolutions [</span>
<span  style="font-size: 9.962599754333496px;">18</span><span  style="font-size: 10.061732292175293px;">], increasing the length of the longest paths</span>
<span  style="font-size: 10.012289047241211px;">between any two positions in the network. Convolutional layers are generally more expensive than</span>
<span  style="font-size: 10.061732292175293px;">recurrent layers, by a factor of</span>
<span  style="font-size: 9.962599754333496px;"> k</span><span  style="font-size: 10.061732292175293px;">. Separable convolutions [</span>
<span  style="font-size: 9.962599754333496px;">6</span><span  style="font-size: 10.061732292175293px;">], however, decrease the complexity</span>
<span  style="font-size: 10.061732292175293px;">considerably, to</span>
<span  style="font-size: 9.962599754333496px;"> O</span><span  style="font-size: 9.962599754333496px;">(</span><span  style="font-size: 9.962599754333496px;">k</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> n</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.962599754333496px;"> +</span><span  style="font-size: 9.962599754333496px;"> n</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 10.061732292175293px;">. Even with</span>
<span  style="font-size: 9.962599754333496px;"> k</span><span  style="font-size: 9.962599754333496px;"> =</span><span  style="font-size: 9.962599754333496px;"> n</span><span  style="font-size: 10.061732292175293px;">, however, the complexity of a separable</span>
<span  style="font-size: 9.962599754333496px;">the approach we take in our model.</span>
<span  style="font-size: 9.962599754333496px;">and semantic structure of the sentences.</span>
<span  style="font-size: 11.9552001953125px;">5</span>
<span  style="font-size: 11.9552001953125px;">Training</span>

<span  style="font-size: 9.962599754333496px;">This section describes the training regime for our models.</span>
<span  style="font-size: 9.962599754333496px;">5.1</span><span  style="font-size: 9.962599754333496px;">Training Data and Batching</span>
<span  style="font-size: 10.061732292175293px;">We trained on the standard WMT 2014 English-German dataset consisting of about 4.5 million</span>
<span  style="font-size: 10.061732292175293px;">sentence pairs. Sentences were encoded using byte-pair encoding [</span>
<span  style="font-size: 9.962599754333496px;">3</span><span  style="font-size: 10.061732292175293px;">], which has a shared source-</span>
<span  style="font-size: 9.987475395202637px;">2014 English-French dataset consisting of 36M sentences and split tokens into a 32000 word-piece</span>
<span  style="font-size: 9.962599754333496px;">38</span><span  style="font-size: 10.061732292175293px;">batch contained a set of sentence pairs containing approximately 25000 source tokens and 25000</span>
<span  style="font-size: 9.962599754333496px;">target tokens.</span>
<span  style="font-size: 9.962599754333496px;">5.2</span><span  style="font-size: 9.962599754333496px;">Hardware and Schedule</span>
<span  style="font-size: 10.061732292175293px;">We trained our models on one machine with 8 NVIDIA P100 GPUs. For our base models using</span>
<span  style="font-size: 9.982504844665527px;">the hyperparameters described throughout the paper, each training step took about 0.4 seconds. We</span>
<span  style="font-size: 10.061732292175293px;">bottom line of table 3), step time was 1.0 seconds. The big models were trained for 300,000 steps</span>
<span  style="font-size: 9.962599754333496px;">(3.5 days).</span>
<span  style="font-size: 9.962599754333496px;">5.3</span><span  style="font-size: 9.962599754333496px;">Optimizer</span>
<span  style="font-size: 10.041984558105469px;">We used the Adam optimizer [</span>
<span  style="font-size: 9.962599754333496px;">20</span><span  style="font-size: 10.041984558105469px;">] with</span>
<span  style="font-size: 9.962599754333496px;"> β</span><span  style="font-size: 9.962599754333496px;"> = 0</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">9</span><span  style="font-size: 10.041984558105469px;">,</span>
<span  style="font-size: 9.962599754333496px;"> β</span><span  style="font-size: 9.962599754333496px;"> = 0</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">98</span><span  style="font-size: 10.041984558105469px;"> and</span>
<span  style="font-size: 9.962599754333496px;"> ϵ</span><span  style="font-size: 9.962599754333496px;"> = 10</span><span  style="font-size: 10.041984558105469px;">. We varied the learning</span>
<span  style="font-size: 9.962599754333496px;">rate over the course of training, according to the formula:</span>
<span  style="font-size: 9.962599754333496px;">lrate</span><span  style="font-size: 9.962599754333496px;"> =</span><span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.962599754333496px;"> </span><span  style="font-size: 9.962599754333496px;">·</span><span  style="font-size: 9.962599754333496px;"> min(</span><span  style="font-size: 9.962599754333496px;">step</span><span  style="font-size: 9.962599754333496px;">_</span><span  style="font-size: 9.962599754333496px;">num</span><span  style="font-size: 9.962599754333496px;">, step</span><span  style="font-size: 9.962599754333496px;">_</span><span  style="font-size: 9.962599754333496px;">num</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> warmup</span><span  style="font-size: 9.962599754333496px;">_</span><span  style="font-size: 9.962599754333496px;">steps</span><span  style="font-size: 9.962599754333496px;">)</span><span  style="font-size: 9.962599754333496px;">(3)</span>
<span  style="font-size: 10.017244338989258px;">This corresponds to increasing the learning rate linearly for the ﬁrst</span>
<span  style="font-size: 9.962599754333496px;"> warmup</span><span  style="font-size: 9.962599754333496px;">_</span><span  style="font-size: 9.962599754333496px;">steps</span><span  style="font-size: 10.017244338989258px;"> training steps,</span>
<span  style="font-size: 10.061732292175293px;">and decreasing it thereafter proportionally to the inverse square root of the step number. We used</span>
<span  style="font-size: 9.962599754333496px;">warmup</span><span  style="font-size: 9.962599754333496px;">_</span><span  style="font-size: 9.962599754333496px;">steps</span><span  style="font-size: 9.962599754333496px;"> = 4000</span><span  style="font-size: 9.962599754333496px;">.</span>
<span  style="font-size: 9.962599754333496px;">5.4</span><span  style="font-size: 9.962599754333496px;">Regularization</span>
<span  style="font-size: 9.962599754333496px;">We employ three types of regularization during training:</span>
<span  style="font-size: 9.962599754333496px;">Residual Dropout</span><span  style="font-size: 9.962599754333496px;">33</span><span  style="font-size: 10.061732292175293px;">positional encodings in both the encoder and decoder stacks. For the base model, we use a rate of</span>
<span  style="font-size: 9.962599754333496px;">P</span><span  style="font-size: 9.962599754333496px;"> = 0</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">1</span><span  style="font-size: 9.962599754333496px;">.</span>
<span  style="font-size: 9.962599754333496px;">7</span>
<span  style="font-size: 9.962599754333496px;">Table 2: The Transformer achieves better BLEU scores than previous state-of-the-art models on the</span><span  style="font-size: 9.962599754333496px;">English-to-German and English-to-French newstest2014 tests at a fraction of the training cost.</span>
<span  style="font-size: 9.962599754333496px;">Model</span><span  style="font-size: 9.962599754333496px;">BLEU</span><span  style="font-size: 9.962599754333496px;">Training Cost (FLOPs)</span>
<span  style="font-size: 9.962599754333496px;">EN-DE</span><span  style="font-size: 9.962599754333496px;">EN-FR</span><span  style="font-size: 9.962599754333496px;">EN-DE</span><span  style="font-size: 9.962599754333496px;">EN-FR</span>
<span  style="font-size: 9.962599754333496px;">ByteNet [18]</span><span  style="font-size: 9.962599754333496px;">23.75</span><span  style="font-size: 9.962599754333496px;">Deep-Att + PosUnk [39]</span><span  style="font-size: 9.962599754333496px;">39.2</span><span  style="font-size: 9.962599754333496px;">1</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">0</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span>
<span  style="font-size: 9.962599754333496px;">GNMT + RL [38]</span><span  style="font-size: 9.962599754333496px;">24.6</span><span  style="font-size: 9.962599754333496px;">39.92</span><span  style="font-size: 9.962599754333496px;">2</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">3</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span><span  style="font-size: 9.962599754333496px;">1</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">4</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span>
<span  style="font-size: 9.962599754333496px;">ConvS2S [9]</span><span  style="font-size: 9.962599754333496px;">25.16</span><span  style="font-size: 9.962599754333496px;">40.46</span><span  style="font-size: 9.962599754333496px;">9</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">6</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span><span  style="font-size: 9.962599754333496px;">1</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">5</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span>
<span  style="font-size: 9.962599754333496px;">MoE [32]</span><span  style="font-size: 9.962599754333496px;">26.03</span><span  style="font-size: 9.962599754333496px;">40.56</span><span  style="font-size: 9.962599754333496px;">2</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">0</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span><span  style="font-size: 9.962599754333496px;">1</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">2</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span>
<span  style="font-size: 9.962599754333496px;">Deep-Att + PosUnk Ensemble [39]</span><span  style="font-size: 9.962599754333496px;">40.4</span><span  style="font-size: 9.962599754333496px;">8</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">0</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span>
<span  style="font-size: 9.962599754333496px;">GNMT + RL Ensemble [38]</span><span  style="font-size: 9.962599754333496px;">26.30</span><span  style="font-size: 9.962599754333496px;">41.16</span><span  style="font-size: 9.962599754333496px;">1</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">8</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span><span  style="font-size: 9.962599754333496px;">1</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">1</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span>
<span  style="font-size: 9.962599754333496px;">ConvS2S Ensemble [9]</span><span  style="font-size: 9.962599754333496px;">26.36</span><span  style="font-size: 9.962599754333496px;">41.29</span><span  style="font-size: 9.962599754333496px;">7</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">7</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span><span  style="font-size: 9.962599754333496px;">1</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">2</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span>
<span  style="font-size: 9.962599754333496px;">Transformer (base model)</span><span  style="font-size: 9.962599754333496px;">27.3</span><span  style="font-size: 9.962599754333496px;">38.1</span><span  style="font-size: 9.962599754333496px;">3</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">3</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span>
<span  style="font-size: 9.962599754333496px;">Transformer (big)</span><span  style="font-size: 9.962599754333496px;">28.4</span><span  style="font-size: 9.962599754333496px;">41.8</span><span  style="font-size: 9.962599754333496px;">2</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">3</span><span  style="font-size: 9.962599754333496px;"> ·</span><span  style="font-size: 9.962599754333496px;"> 10</span>
<span  style="font-size: 9.962599754333496px;">Label Smoothing</span><span  style="font-size: 10.061732292175293px;">During training, we employed label smoothing of value</span>
<span  style="font-size: 9.962599754333496px;"> ϵ</span><span  style="font-size: 9.962599754333496px;"> = 0</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">1</span><span  style="font-size: 10.061732292175293px;"> [</span>
<span  style="font-size: 9.962599754333496px;">36</span><span  style="font-size: 10.061732292175293px;">]. This</span>
<span  style="font-size: 9.962599754333496px;">hurts perplexity, as the model learns to be more unsure, but improves accuracy and BLEU score.</span>
<span  style="font-size: 11.9552001953125px;">6</span>
<span  style="font-size: 11.9552001953125px;">Results</span>

<span  style="font-size: 9.962599754333496px;">6.1</span><span  style="font-size: 9.962599754333496px;">Machine Translation</span>
<span  style="font-size: 9.962599754333496px;"> 2</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">0</span><span  style="font-size: 10.051863670349121px;">BLEU, establishing a new state-of-the-art BLEU score of</span>
<span  style="font-size: 9.962599754333496px;"> 28</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">4</span><span  style="font-size: 10.051863670349121px;">. The conﬁguration of this model is</span>
<span  style="font-size: 10.032095909118652px;">listed in the bottom line of Table 3. Training took</span>
<span  style="font-size: 9.962599754333496px;"> 3</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">5</span><span  style="font-size: 10.032095909118652px;"> days on</span>
<span  style="font-size: 9.962599754333496px;"> 8</span><span  style="font-size: 10.032095909118652px;"> P100 GPUs. Even our base model</span>
<span  style="font-size: 9.962599754333496px;">surpasses all previously published models and ensembles, at a fraction of the training cost of any of</span><span  style="font-size: 9.962599754333496px;">the competitive models.</span>
<span  style="font-size: 9.962599754333496px;"> 41</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">0</span><span  style="font-size: 9.962599754333496px;"> 1</span><span  style="font-size: 9.962599754333496px;">/</span><span  style="font-size: 9.962599754333496px;">4</span><span  style="font-size: 10.061732292175293px;">previous state-of-the-art model. The Transformer (big) model trained for English-to-French used</span>
<span  style="font-size: 9.962599754333496px;">dropout rate</span><span  style="font-size: 9.962599754333496px;"> P</span><span  style="font-size: 9.962599754333496px;"> = 0</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">1</span><span  style="font-size: 9.962599754333496px;">, instead of</span><span  style="font-size: 9.962599754333496px;"> 0</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">3</span><span  style="font-size: 9.962599754333496px;">.</span>
<span  style="font-size: 10.061732292175293px;">For the base models, we used a single model obtained by averaging the last 5 checkpoints, which</span>
<span  style="font-size: 10.061732292175293px;">were written at 10-minute intervals. For the big models, we averaged the last 20 checkpoints. We</span>
<span  style="font-size: 10.061732292175293px;">used beam search with a beam size of</span>
<span  style="font-size: 9.962599754333496px;"> 4</span><span  style="font-size: 10.061732292175293px;"> and length penalty</span>
<span  style="font-size: 9.962599754333496px;"> α</span><span  style="font-size: 9.962599754333496px;"> = 0</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">6</span><span  style="font-size: 10.061732292175293px;"> [</span>
<span  style="font-size: 9.962599754333496px;">38</span><span  style="font-size: 10.061732292175293px;">]. These hyperparameters</span>
<span  style="font-size: 9.962599754333496px;">inference to input length +</span><span  style="font-size: 9.962599754333496px;"> 50</span><span  style="font-size: 9.962599754333496px;">, but terminate early when possible [38].</span>
<span  style="font-size: 9.982504844665527px;">model by multiplying the training time, the number of GPUs used, and an estimate of the sustained</span>
<span  style="font-size: 9.962599754333496px;">single-precision ﬂoating-point capacity of each GPU</span><span  style="font-size: 9.962599754333496px;">.</span>
<span  style="font-size: 9.962599754333496px;">6.2</span><span  style="font-size: 9.962599754333496px;">Model Variations</span>
<span  style="font-size: 10.056798934936523px;">To evaluate the importance of different components of the Transformer, we varied our base model</span>
<span  style="font-size: 10.061732292175293px;">in different ways, measuring the change in performance on English-to-German translation on the</span>
<span  style="font-size: 10.061732292175293px;">development set, newstest2013. We used beam search as described in the previous section, but no</span>
<span  style="font-size: 9.962599754333496px;">checkpoint averaging. We present these results in Table 3.</span>
<span  style="font-size: 10.061732292175293px;">keeping the amount of computation constant, as described in Section 3.2.2. While single-head</span>
<span  style="font-size: 9.962599754333496px;">attention is 0.9 BLEU worse than the best setting, quality also drops off with too many heads.</span>

<span  style="font-size: 9.962599754333496px;">8</span>
<span  style="font-size: 9.962599754333496px;">perplexities are per-wordpiece, according to our byte-pair encoding, and should not be compared to</span><span  style="font-size: 9.962599754333496px;">per-word perplexities.</span>
<span  style="font-size: 9.962599754333496px;">N</span><span  style="font-size: 9.962599754333496px;">d</span><span  style="font-size: 9.962599754333496px;">d</span><span  style="font-size: 9.962599754333496px;">h</span><span  style="font-size: 9.962599754333496px;">d</span><span  style="font-size: 9.962599754333496px;">d</span><span  style="font-size: 9.962599754333496px;">P</span><span  style="font-size: 9.962599754333496px;">ϵ</span><span  style="font-size: 9.962599754333496px;">train</span><span  style="font-size: 9.962599754333496px;">PPL</span><span  style="font-size: 9.962599754333496px;">BLEU</span><span  style="font-size: 9.962599754333496px;">params</span>
<span  style="font-size: 9.962599754333496px;">steps</span><span  style="font-size: 9.962599754333496px;">(dev)</span><span  style="font-size: 9.962599754333496px;">(dev)</span><span  style="font-size: 9.962599754333496px;">×</span><span  style="font-size: 9.962599754333496px;">10</span>
<span  style="font-size: 9.962599754333496px;">base</span><span  style="font-size: 9.962599754333496px;">6</span><span  style="font-size: 9.962599754333496px;">512</span><span  style="font-size: 9.962599754333496px;">2048</span><span  style="font-size: 9.962599754333496px;">8</span><span  style="font-size: 9.962599754333496px;">64</span><span  style="font-size: 9.962599754333496px;">64</span><span  style="font-size: 9.962599754333496px;">0.1</span><span  style="font-size: 9.962599754333496px;">0.1</span><span  style="font-size: 9.962599754333496px;">100K</span><span  style="font-size: 9.962599754333496px;">4.92</span><span  style="font-size: 9.962599754333496px;">25.8</span><span  style="font-size: 9.962599754333496px;">65</span>
<span  style="font-size: 9.962599754333496px;">(A)</span>
<span  style="font-size: 9.962599754333496px;">1</span><span  style="font-size: 9.962599754333496px;">512</span><span  style="font-size: 9.962599754333496px;">512</span><span  style="font-size: 9.962599754333496px;">5.29</span><span  style="font-size: 9.962599754333496px;">24.9</span>
<span  style="font-size: 9.962599754333496px;">4</span><span  style="font-size: 9.962599754333496px;">128</span><span  style="font-size: 9.962599754333496px;">128</span><span  style="font-size: 9.962599754333496px;">5.00</span><span  style="font-size: 9.962599754333496px;">25.5</span>
<span  style="font-size: 9.962599754333496px;">16</span><span  style="font-size: 9.962599754333496px;">32</span><span  style="font-size: 9.962599754333496px;">32</span><span  style="font-size: 9.962599754333496px;">4.91</span><span  style="font-size: 9.962599754333496px;">25.8</span>
<span  style="font-size: 9.962599754333496px;">32</span><span  style="font-size: 9.962599754333496px;">16</span><span  style="font-size: 9.962599754333496px;">16</span><span  style="font-size: 9.962599754333496px;">5.01</span><span  style="font-size: 9.962599754333496px;">25.4</span>
<span  style="font-size: 9.962599754333496px;">(B)</span><span  style="font-size: 9.962599754333496px;">16</span><span  style="font-size: 9.962599754333496px;">5.16</span><span  style="font-size: 9.962599754333496px;">25.1</span><span  style="font-size: 9.962599754333496px;">58</span>
<span  style="font-size: 9.962599754333496px;">32</span><span  style="font-size: 9.962599754333496px;">5.01</span><span  style="font-size: 9.962599754333496px;">25.4</span><span  style="font-size: 9.962599754333496px;">60</span>
<span  style="font-size: 9.962599754333496px;">(C)</span>
<span  style="font-size: 9.962599754333496px;">2</span><span  style="font-size: 9.962599754333496px;">6.11</span><span  style="font-size: 9.962599754333496px;">23.7</span><span  style="font-size: 9.962599754333496px;">36</span>
<span  style="font-size: 9.962599754333496px;">4</span><span  style="font-size: 9.962599754333496px;">5.19</span><span  style="font-size: 9.962599754333496px;">25.3</span><span  style="font-size: 9.962599754333496px;">50</span>
<span  style="font-size: 9.962599754333496px;">8</span><span  style="font-size: 9.962599754333496px;">4.88</span><span  style="font-size: 9.962599754333496px;">25.5</span><span  style="font-size: 9.962599754333496px;">80</span>
<span  style="font-size: 9.962599754333496px;">256</span><span  style="font-size: 9.962599754333496px;">32</span><span  style="font-size: 9.962599754333496px;">32</span><span  style="font-size: 9.962599754333496px;">5.75</span><span  style="font-size: 9.962599754333496px;">24.5</span><span  style="font-size: 9.962599754333496px;">28</span>
<span  style="font-size: 9.962599754333496px;">1024</span><span  style="font-size: 9.962599754333496px;">128</span><span  style="font-size: 9.962599754333496px;">128</span><span  style="font-size: 9.962599754333496px;">4.66</span><span  style="font-size: 9.962599754333496px;">26.0</span><span  style="font-size: 9.962599754333496px;">168</span>
<span  style="font-size: 9.962599754333496px;">1024</span><span  style="font-size: 9.962599754333496px;">5.12</span><span  style="font-size: 9.962599754333496px;">25.4</span><span  style="font-size: 9.962599754333496px;">53</span>
<span  style="font-size: 9.962599754333496px;">4096</span><span  style="font-size: 9.962599754333496px;">4.75</span><span  style="font-size: 9.962599754333496px;">26.2</span><span  style="font-size: 9.962599754333496px;">90</span>
<span  style="font-size: 9.962599754333496px;">(D)</span>
<span  style="font-size: 9.962599754333496px;">0.0</span><span  style="font-size: 9.962599754333496px;">5.77</span><span  style="font-size: 9.962599754333496px;">24.6</span>
<span  style="font-size: 9.962599754333496px;">0.2</span><span  style="font-size: 9.962599754333496px;">4.95</span><span  style="font-size: 9.962599754333496px;">25.5</span>
<span  style="font-size: 9.962599754333496px;">0.0</span><span  style="font-size: 9.962599754333496px;">4.67</span><span  style="font-size: 9.962599754333496px;">25.3</span>
<span  style="font-size: 9.962599754333496px;">0.2</span><span  style="font-size: 9.962599754333496px;">5.47</span><span  style="font-size: 9.962599754333496px;">25.7</span>
<span  style="font-size: 9.962599754333496px;">(E)</span><span  style="font-size: 9.962599754333496px;">positional embedding instead of sinusoids</span><span  style="font-size: 9.962599754333496px;">4.92</span><span  style="font-size: 9.962599754333496px;">25.7</span>
<span  style="font-size: 9.962599754333496px;">big</span><span  style="font-size: 9.962599754333496px;">6</span><span  style="font-size: 9.962599754333496px;">1024</span><span  style="font-size: 9.962599754333496px;">4096</span><span  style="font-size: 9.962599754333496px;">16</span><span  style="font-size: 9.962599754333496px;">0.3</span><span  style="font-size: 9.962599754333496px;">300K</span><span  style="font-size: 9.962599754333496px;">4.33</span><span  style="font-size: 9.962599754333496px;">26.4</span><span  style="font-size: 9.962599754333496px;">213</span>
<span  style="font-size: 9.962599754333496px;">of WSJ)</span>
<span  style="font-size: 9.962599754333496px;">Parser</span><span  style="font-size: 9.962599754333496px;">Training</span><span  style="font-size: 9.962599754333496px;">WSJ 23 F1</span>
<span  style="font-size: 9.962599754333496px;">Vinyals & Kaiser el al. (2014) [37]</span><span  style="font-size: 9.962599754333496px;">WSJ only, discriminative</span><span  style="font-size: 9.962599754333496px;">88.3</span><span  style="font-size: 9.962599754333496px;">Petrov et al. (2006) [29]</span><span  style="font-size: 9.962599754333496px;">WSJ only, discriminative</span><span  style="font-size: 9.962599754333496px;">90.4</span><span  style="font-size: 9.962599754333496px;">Zhu et al. (2013) [40]</span><span  style="font-size: 9.962599754333496px;">WSJ only, discriminative</span><span  style="font-size: 9.962599754333496px;">90.4</span><span  style="font-size: 9.962599754333496px;">Dyer et al. (2016) [8]</span><span  style="font-size: 9.962599754333496px;">WSJ only, discriminative</span><span  style="font-size: 9.962599754333496px;">91.7</span>
<span  style="font-size: 9.962599754333496px;">Transformer (4 layers)</span><span  style="font-size: 9.962599754333496px;">WSJ only, discriminative</span><span  style="font-size: 9.962599754333496px;">91.3</span>
<span  style="font-size: 9.962599754333496px;">Zhu et al. (2013) [40]</span><span  style="font-size: 9.962599754333496px;">semi-supervised</span><span  style="font-size: 9.962599754333496px;">91.3</span><span  style="font-size: 9.962599754333496px;">Huang & Harper (2009) [14]</span><span  style="font-size: 9.962599754333496px;">semi-supervised</span><span  style="font-size: 9.962599754333496px;">91.3</span><span  style="font-size: 9.962599754333496px;">McClosky et al. (2006) [26]</span><span  style="font-size: 9.962599754333496px;">semi-supervised</span><span  style="font-size: 9.962599754333496px;">92.1</span><span  style="font-size: 9.962599754333496px;">Vinyals & Kaiser el al. (2014) [37]</span><span  style="font-size: 9.962599754333496px;">semi-supervised</span><span  style="font-size: 9.962599754333496px;">92.1</span>
<span  style="font-size: 9.962599754333496px;">Transformer (4 layers)</span><span  style="font-size: 9.962599754333496px;">semi-supervised</span><span  style="font-size: 9.962599754333496px;">92.7</span>
<span  style="font-size: 9.962599754333496px;">Luong et al. (2015) [23]</span><span  style="font-size: 9.962599754333496px;">multi-task</span><span  style="font-size: 9.962599754333496px;">93.0</span><span  style="font-size: 9.962599754333496px;">Dyer et al. (2016) [8]</span><span  style="font-size: 9.962599754333496px;">generative</span><span  style="font-size: 9.962599754333496px;">93.3</span>
<span  style="font-size: 10.061732292175293px;">In Table 3 rows (B), we observe that reducing the attention key size</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 10.061732292175293px;"> hurts model quality. This</span>
<span  style="font-size: 10.061732292175293px;">suggests that determining compatibility is not easy and that a more sophisticated compatibility</span>
<span  style="font-size: 9.962599754333496px;">9</span><span  style="font-size: 9.962599754333496px;">results to the base model.</span>
<span  style="font-size: 9.962599754333496px;">6.3</span><span  style="font-size: 9.962599754333496px;">English Constituency Parsing</span>
<span  style="font-size: 10.041984558105469px;">To evaluate if the Transformer can generalize to other tasks we performed experiments on English</span>

<span  style="font-size: 9.962599754333496px;">9</span>
<span  style="font-size: 10.061732292175293px;">constraints and is signiﬁcantly longer than the input. Furthermore, RNN sequence-to-sequence</span>
<span  style="font-size: 9.962599754333496px;">models have not been able to attain state-of-the-art results in small-data regimes [37].</span>
<span  style="font-size: 9.962599754333496px;"> d</span><span  style="font-size: 9.962599754333496px;"> = 1024</span><span  style="font-size: 10.051863670349121px;">Penn Treebank [</span>
<span  style="font-size: 9.962599754333496px;">25</span><span  style="font-size: 10.051863670349121px;">], about 40K training sentences. We also trained it in a semi-supervised setting,</span>
<span  style="font-size: 9.962599754333496px;">37</span><span  style="font-size: 9.962599754333496px;">for the semi-supervised setting.</span>
<span  style="font-size: 10.041984558105469px;">(section 5.4), learning rates and beam size on the Section 22 development set, all other parameters</span>
<span  style="font-size: 10.061732292175293px;">remained unchanged from the English-to-German base translation model. During inference, we</span>
<span  style="font-size: 9.962599754333496px;"> 300</span><span  style="font-size: 9.962599754333496px;"> 21</span><span  style="font-size: 9.962599754333496px;"> α</span><span  style="font-size: 9.962599754333496px;"> = 0</span><span  style="font-size: 9.962599754333496px;">.</span><span  style="font-size: 9.962599754333496px;">3</span><span  style="font-size: 9.962599754333496px;">for both WSJ only and the semi-supervised setting.</span>
<span  style="font-size: 10.061732292175293px;">Our results in Table 4 show that despite the lack of task-speciﬁc tuning our model performs sur-</span>
<span  style="font-size: 10.032095909118652px;">prisingly well, yielding better results than all previously reported models with the exception of the</span>
<span  style="font-size: 9.962599754333496px;">Recurrent Neural Network Grammar [8].</span>
<span  style="font-size: 10.032095909118652px;">In contrast to RNN sequence-to-sequence models [</span>
<span  style="font-size: 9.962599754333496px;">37</span><span  style="font-size: 10.032095909118652px;">], the Transformer outperforms the Berkeley-</span>
<span  style="font-size: 9.962599754333496px;">Parser [29] even when training only on the WSJ training set of 40K sentences.</span>
<span  style="font-size: 11.9552001953125px;">7</span>
<span  style="font-size: 11.9552001953125px;">Conclusion</span>

<span  style="font-size: 9.972557067871094px;">In this work, we presented the Transformer, the ﬁrst sequence transduction model based entirely on</span>
<span  style="font-size: 9.962599754333496px;">multi-headed self-attention.</span>
<span  style="font-size: 10.061732292175293px;">For translation tasks, the Transformer can be trained signiﬁcantly faster than architectures based</span>
<span  style="font-size: 10.061732292175293px;">on recurrent or convolutional layers. On both WMT 2014 English-to-German and WMT 2014</span>
<span  style="font-size: 10.061732292175293px;">English-to-French translation tasks, we achieve a new state of the art. In the former task our best</span>
<span  style="font-size: 9.962599754333496px;">model outperforms even all previously reported ensembles.</span>
<span  style="font-size: 10.061732292175293px;">to investigate local, restricted attention mechanisms to efﬁciently handle large inputs and outputs</span>

<span  style="font-size: 10.061732292175293px;">The code we used to train and evaluate our models is available at</span>
<span  style="font-size: 9.962599754333496px;"> https://github.com/</span><span  style="font-size: 9.962599754333496px;">tensorflow/tensor2tensor</span><span  style="font-size: 9.962599754333496px;">.</span>
<span  style="font-size: 9.962599754333496px;">Acknowledgements</span><span  style="font-size: 10.061732292175293px;">We are grateful to Nal Kalchbrenner and Stephan Gouws for their fruitful</span>
<span  style="font-size: 9.962599754333496px;">comments, corrections and inspiration.</span>
<span  style="font-size: 11.9552001953125px;">References</span>

<span  style="font-size: 9.962599754333496px;">[1]</span><span  style="font-size: 9.962599754333496px;">arXiv:1607.06450</span><span  style="font-size: 9.962599754333496px;">, 2016.</span>
<span  style="font-size: 9.962599754333496px;">[2]</span><span  style="font-size: 9.962599754333496px;">learning to align and translate.</span><span  style="font-size: 9.962599754333496px;"> CoRR</span><span  style="font-size: 9.962599754333496px;">, abs/1409.0473, 2014.</span>
<span  style="font-size: 9.962599754333496px;">[3]</span><span  style="font-size: 9.962599754333496px;">machine translation architectures.</span><span  style="font-size: 9.962599754333496px;"> CoRR</span><span  style="font-size: 9.962599754333496px;">, abs/1703.03906, 2017.</span>
<span  style="font-size: 9.962599754333496px;">[4]</span><span  style="font-size: 9.962599754333496px;">reading.</span><span  style="font-size: 9.962599754333496px;"> arXiv preprint arXiv:1601.06733</span><span  style="font-size: 9.962599754333496px;">, 2016.</span>
<span  style="font-size: 9.962599754333496px;">[5]</span><span  style="font-size: 10.061732292175293px;"> Kyunghyun Cho, Bart van Merrienboer, Caglar Gulcehre, Fethi Bougares, Holger Schwenk,</span>
<span  style="font-size: 9.972557067871094px;">and Yoshua Bengio. Learning phrase representations using rnn encoder-decoder for statistical</span>
<span  style="font-size: 9.962599754333496px;">machine translation.</span><span  style="font-size: 9.962599754333496px;"> CoRR</span><span  style="font-size: 9.962599754333496px;">, abs/1406.1078, 2014.</span>
<span  style="font-size: 9.962599754333496px;">[6]</span><span  style="font-size: 10.061732292175293px;"> Francois Chollet. Xception: Deep learning with depthwise separable convolutions.</span>
<span  style="font-size: 10.061732292175293px;"> arXiv</span>
<span  style="font-size: 9.962599754333496px;">preprint arXiv:1610.02357</span><span  style="font-size: 9.962599754333496px;">, 2016.</span>
<span  style="font-size: 9.962599754333496px;">10</span>
<span  style="font-size: 9.962599754333496px;">[7]</span><span  style="font-size: 9.962599754333496px;">of gated recurrent neural networks on sequence modeling.</span><span  style="font-size: 9.962599754333496px;"> CoRR</span><span  style="font-size: 9.962599754333496px;">, abs/1412.3555, 2014.</span>
<span  style="font-size: 9.962599754333496px;">[8]</span><span  style="font-size: 10.061732292175293px;"> Chris Dyer, Adhiguna Kuncoro, Miguel Ballesteros, and Noah A. Smith. Recurrent neural</span>
<span  style="font-size: 9.962599754333496px;">network grammars. In</span><span  style="font-size: 9.962599754333496px;"> Proc. of NAACL</span><span  style="font-size: 9.962599754333496px;">, 2016.</span>
<span  style="font-size: 9.962599754333496px;">[9]</span><span  style="font-size: 10.022196769714355px;"> Jonas Gehring, Michael Auli, David Grangier, Denis Yarats, and Yann N. Dauphin. Convolu-</span>
<span  style="font-size: 9.962599754333496px;">tional sequence to sequence learning.</span><span  style="font-size: 9.962599754333496px;"> arXiv preprint arXiv:1705.03122v2</span><span  style="font-size: 9.962599754333496px;">, 2017.</span>
<span  style="font-size: 9.962599754333496px;">[10]</span><span  style="font-size: 10.061732292175293px;"> Alex Graves.</span>
<span  style="font-size: 10.061732292175293px;">Generating sequences with recurrent neural networks.</span>
<span  style="font-size: 10.061732292175293px;">arXiv preprint</span>
<span  style="font-size: 9.962599754333496px;">arXiv:1308.0850</span><span  style="font-size: 9.962599754333496px;">, 2013.</span>
<span  style="font-size: 9.962599754333496px;">[11]</span><span  style="font-size: 10.061732292175293px;"> Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for im-</span>
<span  style="font-size: 10.061732292175293px;">age recognition. In</span>
<span  style="font-size: 10.061732292175293px;"> Proceedings of the IEEE Conference on Computer Vision and Pattern</span>
<span  style="font-size: 9.962599754333496px;">Recognition</span><span  style="font-size: 9.962599754333496px;">, pages 770–778, 2016.</span>
<span  style="font-size: 9.962599754333496px;">[12]</span><span  style="font-size: 10.041984558105469px;"> Sepp Hochreiter, Yoshua Bengio, Paolo Frasconi, and Jürgen Schmidhuber. Gradient ﬂow in</span>
<span  style="font-size: 9.962599754333496px;">recurrent nets: the difﬁculty of learning long-term dependencies, 2001.</span>
<span  style="font-size: 9.962599754333496px;">[13]</span><span  style="font-size: 10.061732292175293px;"> Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory.</span>
<span  style="font-size: 10.061732292175293px;"> Neural computation</span>
<span  style="font-size: 10.061732292175293px;">,</span>
<span  style="font-size: 9.962599754333496px;">9(8):1735–1780, 1997.</span>
<span  style="font-size: 9.962599754333496px;">[14]</span><span  style="font-size: 10.061732292175293px;"> Zhongqiang Huang and Mary Harper. Self-training PCFG grammars with latent annotations</span>
<span  style="font-size: 10.061732292175293px;">across languages. In</span>
<span  style="font-size: 10.061732292175293px;"> Proceedings of the 2009 Conference on Empirical Methods in Natural</span>
<span  style="font-size: 9.962599754333496px;">Language Processing</span><span  style="font-size: 9.962599754333496px;">, pages 832–841. ACL, August 2009.</span>
<span  style="font-size: 9.962599754333496px;">[15]</span><span  style="font-size: 10.022196769714355px;"> Rafal Jozefowicz, Oriol Vinyals, Mike Schuster, Noam Shazeer, and Yonghui Wu. Exploring</span>
<span  style="font-size: 9.962599754333496px;">the limits of language modeling.</span><span  style="font-size: 9.962599754333496px;"> arXiv preprint arXiv:1602.02410</span><span  style="font-size: 9.962599754333496px;">, 2016.</span>
<span  style="font-size: 9.962599754333496px;">[16]</span><span  style="font-size: 9.962599754333496px;">Information Processing Systems, (NIPS)</span><span  style="font-size: 9.962599754333496px;">, 2016.</span>
<span  style="font-size: 9.962599754333496px;">[17]</span><span  style="font-size: 9.962599754333496px;">on Learning Representations (ICLR)</span><span  style="font-size: 9.962599754333496px;">, 2016.</span>
<span  style="font-size: 9.962599754333496px;">[18]</span><span  style="font-size: 9.962599754333496px;">2017.</span>
<span  style="font-size: 9.962599754333496px;">[19]</span><span  style="font-size: 9.962599754333496px;">In</span><span  style="font-size: 9.962599754333496px;"> International Conference on Learning Representations</span><span  style="font-size: 9.962599754333496px;">, 2017.</span>
<span  style="font-size: 9.962599754333496px;">[20]</span>
<span  style="font-size: 9.962599754333496px;">[21]</span><span  style="font-size: 9.962599754333496px;">arXiv:1703.10722</span><span  style="font-size: 9.962599754333496px;">, 2017.</span>
<span  style="font-size: 9.962599754333496px;">[22]</span><span  style="font-size: 10.061732292175293px;"> Zhouhan Lin, Minwei Feng, Cicero Nogueira dos Santos, Mo Yu, Bing Xiang, Bowen</span>
<span  style="font-size: 10.061732292175293px;">Zhou, and Yoshua Bengio. A structured self-attentive sentence embedding.</span>
<span  style="font-size: 10.061732292175293px;"> arXiv preprint</span>
<span  style="font-size: 9.962599754333496px;">arXiv:1703.03130</span><span  style="font-size: 9.962599754333496px;">, 2017.</span>
<span  style="font-size: 9.962599754333496px;">[23]</span><span  style="font-size: 9.962599754333496px;">sequence to sequence learning.</span><span  style="font-size: 9.962599754333496px;"> arXiv preprint arXiv:1511.06114</span><span  style="font-size: 9.962599754333496px;">, 2015.</span>
<span  style="font-size: 9.962599754333496px;">[24]</span><span  style="font-size: 9.962599754333496px;">based neural machine translation.</span><span  style="font-size: 9.962599754333496px;"> arXiv preprint arXiv:1508.04025</span><span  style="font-size: 9.962599754333496px;">, 2015.</span>
<span  style="font-size: 9.962599754333496px;">[25]</span><span  style="font-size: 9.962599754333496px;">corpus of english: The penn treebank.</span><span  style="font-size: 9.962599754333496px;"> Computational linguistics</span><span  style="font-size: 9.962599754333496px;">, 19(2):313–330, 1993.</span>
<span  style="font-size: 9.962599754333496px;">[26]</span><span  style="font-size: 9.977532386779785px;"> David McClosky, Eugene Charniak, and Mark Johnson. Effective self-training for parsing. In</span>
<span  style="font-size: 9.962599754333496px;">pages 152–159. ACL, June 2006.</span>
<span  style="font-size: 9.962599754333496px;">11</span>
<span  style="font-size: 9.962599754333496px;">[27]</span><span  style="font-size: 9.962599754333496px;">model. In</span><span  style="font-size: 9.962599754333496px;"> Empirical Methods in Natural Language Processing</span><span  style="font-size: 9.962599754333496px;">, 2016.</span>
<span  style="font-size: 9.962599754333496px;">[28]</span><span  style="font-size: 9.962599754333496px;">summarization.</span><span  style="font-size: 9.962599754333496px;"> arXiv preprint arXiv:1705.04304</span><span  style="font-size: 9.962599754333496px;">, 2017.</span>
<span  style="font-size: 9.962599754333496px;">[29]</span><span  style="font-size: 10.061732292175293px;"> Slav Petrov, Leon Barrett, Romain Thibaux, and Dan Klein. Learning accurate, compact,</span>
<span  style="font-size: 10.061732292175293px;">and interpretable tree annotation. In</span>
<span  style="font-size: 10.061732292175293px;"> Proceedings of the 21st International Conference on</span>
<span  style="font-size: 10.061732292175293px;">Computational Linguistics and 44th Annual Meeting of the ACL</span>
<span  style="font-size: 10.061732292175293px;">, pages 433–440. ACL, July</span>
<span  style="font-size: 9.962599754333496px;">2006.</span>
<span  style="font-size: 9.962599754333496px;">[30]</span><span  style="font-size: 10.061732292175293px;"> Oﬁr Press and Lior Wolf. Using the output embedding to improve language models.</span>
<span  style="font-size: 10.061732292175293px;"> arXiv</span>
<span  style="font-size: 9.962599754333496px;">preprint arXiv:1608.05859</span><span  style="font-size: 9.962599754333496px;">, 2016.</span>
<span  style="font-size: 9.962599754333496px;">[31]</span><span  style="font-size: 9.962599754333496px;">with subword units.</span><span  style="font-size: 9.962599754333496px;"> arXiv preprint arXiv:1508.07909</span><span  style="font-size: 9.962599754333496px;">, 2015.</span>
<span  style="font-size: 9.962599754333496px;">[32]</span><span  style="font-size: 10.061732292175293px;">and Jeff Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts</span>
<span  style="font-size: 9.962599754333496px;">layer.</span><span  style="font-size: 9.962599754333496px;"> arXiv preprint arXiv:1701.06538</span><span  style="font-size: 9.962599754333496px;">, 2017.</span>
<span  style="font-size: 9.962599754333496px;">[33]</span><span  style="font-size: 10.02714729309082px;">nov. Dropout: a simple way to prevent neural networks from overﬁtting.</span>
<span  style="font-size: 10.02714729309082px;"> Journal of Machine</span>
<span  style="font-size: 9.962599754333496px;">Learning Research</span><span  style="font-size: 9.962599754333496px;">, 15(1):1929–1958, 2014.</span>
<span  style="font-size: 9.962599754333496px;">[34]</span><span  style="font-size: 10.061732292175293px;"> Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory</span>
<span  style="font-size: 10.061732292175293px;">networks. In C. Cortes, N. D. Lawrence, D. D. Lee, M. Sugiyama, and R. Garnett, editors,</span>
<span  style="font-size: 9.962599754333496px;">Inc., 2015.</span>
<span  style="font-size: 9.962599754333496px;">[35]</span><span  style="font-size: 10.061732292175293px;"> Ilya Sutskever, Oriol Vinyals, and Quoc VV Le. Sequence to sequence learning with neural</span>
<span  style="font-size: 9.962599754333496px;">networks. In</span><span  style="font-size: 9.962599754333496px;"> Advances in Neural Information Processing Systems</span><span  style="font-size: 9.962599754333496px;">, pages 3104–3112, 2014.</span>
<span  style="font-size: 9.962599754333496px;">[36]</span><span  style="font-size: 10.061732292175293px;"> Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jonathon Shlens, and Zbigniew Wojna.</span>
<span  style="font-size: 9.962599754333496px;">Rethinking the inception architecture for computer vision.</span><span  style="font-size: 9.962599754333496px;"> CoRR</span><span  style="font-size: 9.962599754333496px;">, abs/1512.00567, 2015.</span>
<span  style="font-size: 9.962599754333496px;">[37]</span><span  style="font-size: 10.061732292175293px;"> Vinyals & Kaiser, Koo, Petrov, Sutskever, and Hinton. Grammar as a foreign language. In</span>
<span  style="font-size: 9.962599754333496px;">Advances in Neural Information Processing Systems</span><span  style="font-size: 9.962599754333496px;">, 2015.</span>
<span  style="font-size: 9.962599754333496px;">[38]</span><span  style="font-size: 10.061732292175293px;"> Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V Le, Mohammad Norouzi, Wolfgang</span>
<span  style="font-size: 10.012289047241211px;">translation system: Bridging the gap between human and machine translation.</span>
<span  style="font-size: 10.012289047241211px;"> arXiv preprint</span>
<span  style="font-size: 9.962599754333496px;">arXiv:1609.08144</span><span  style="font-size: 9.962599754333496px;">, 2016.</span>
<span  style="font-size: 9.962599754333496px;">[39]</span><span  style="font-size: 10.061732292175293px;"> Jie Zhou, Ying Cao, Xuguang Wang, Peng Li, and Wei Xu. Deep recurrent models with</span>
<span  style="font-size: 9.962599754333496px;">fast-forward connections for neural machine translation.</span><span  style="font-size: 9.962599754333496px;"> CoRR</span><span  style="font-size: 9.962599754333496px;">, abs/1606.04199, 2016.</span>
<span  style="font-size: 9.962599754333496px;">[40]</span><span  style="font-size: 10.061732292175293px;"> Muhua Zhu, Yue Zhang, Wenliang Chen, Min Zhang, and Jingbo Zhu. Fast and accurate</span>
<span  style="font-size: 9.962599754333496px;">1: Long Papers)</span><span  style="font-size: 9.962599754333496px;">, pages 434–443. ACL, August 2013.</span>
<span  style="font-size: 9.962599754333496px;">12</span>
<span  style="font-size: 11.9552001953125px;">Attention Visualizations</span>
<span  style="font-size: 16.335596084594727px;">Input-Input Layer5</span>



































































<span  style="font-size: 10.061732292175293px;">Figure 3: An example of the attention mechanism following long-distance dependencies in the</span>
<span  style="font-size: 9.972557067871094px;">encoder self-attention in layer 5 of 6. Many of the attention heads attend to a distant dependency of</span>
<span  style="font-size: 9.987475395202637px;">the verb ‘making’, completing the phrase ‘making...more difﬁcult’. Attentions here shown only for</span>
<span  style="font-size: 9.962599754333496px;">the word ‘making’. Different colors represent different heads. Best viewed in color.</span>
<span  style="font-size: 9.962599754333496px;">13</span>
<span  style="font-size: 19.567136764526367px;">Input-Input Layer5</span>























































<span  style="font-size: 19.7869873046875px;">Input-Input Layer5</span>























































<span  style="font-size: 9.962599754333496px;">Figure 4: Two attention heads, also in layer 5 of 6, apparently involved in anaphora resolution. Top:</span><span  style="font-size: 10.002370834350586px;">Full attentions for head 5. Bottom: Isolated attentions from just the word ‘its’ for attention heads 5</span>
<span  style="font-size: 9.962599754333496px;">and 6. Note that the attentions are very sharp for this word.</span>
<span  style="font-size: 9.962599754333496px;">14</span>
<span  style="font-size: 19.618867874145508px;">Input-Input Layer5</span>























































<span  style="font-size: 19.62848663330078px;">Input-Input Layer5</span>























































<span  style="font-size: 10.061732292175293px;">Figure 5: Many of the attention heads exhibit behaviour that seems related to the structure of the</span>
<span  style="font-size: 9.962599754333496px;">at layer 5 of 6. The heads clearly learned to perform different tasks.</span>
<span  style="font-size: 9.962599754333496px;">15</span>
