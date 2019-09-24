/*M///////////////////////////////////////////////////////////////////////////////////////
//
//  IMPORTANT: READ BEFORE DOWNLOADING, COPYING, INSTALLING OR USING.
//
//  By downloading, copying, installing or using the software you agree to this license.
//  If you do not agree to this license, do not download, install,
//  copy or use the software.
//
//
//                           License Agreement
//                For Open Source Computer Vision Library
//
// Copyright (C) 2013, OpenCV Foundation, all rights reserved.
// Third party copyrights are property of their respective owners.
//
// Redistribution and use in source and binary forms, with or without modification,
// are permitted provided that the following conditions are met:
//
//   * Redistribution's of source code must retain the above copyright notice,
//     this list of conditions and the following disclaimer.
//
//   * Redistribution's in binary form must reproduce the above copyright notice,
//     this list of conditions and the following disclaimer in the documentation
//     and/or other materials provided with the distribution.
//
//   * The name of the copyright holders may not be used to endorse or promote products
//     derived from this software without specific prior written permission.
//
// This software is provided by the copyright holders and contributors "as is" and
// any express or implied warranties, including, but not limited to, the implied
// warranties of merchantability and fitness for a particular purpose are disclaimed.
// In no event shall the Intel Corporation or contributors be liable for any direct,
// indirect, incidental, special, exemplary, or consequential damages
// (including, but not limited to, procurement of substitute goods or services;
// loss of use, data, or profits; or business interruption) however caused
// and on any theory of liability, whether in contract, strict liability,
// or tort (including negligence or otherwise) arising in any way out of
// the use of this software, even if advised of the possibility of such damage.
//
//M*/

#ifndef OPENCV_DNN_DNN_ALL_LAYERS_HPP
#define OPENCV_DNN_DNN_ALL_LAYERS_HPP
#include <opencv2/dnn.hpp>

namespace cv {
namespace dnn {
CV__DNN_EXPERIMENTAL_NS_BEGIN
//! @addtogroup dnn
//! @{

/** @defgroup dnnLayerList Partial List of Implemented Layers
  @{
  This subsection of dnn module contains information about bult-in layers and their descriptions.

  Classes listed here, in fact, provides C++ API for creating intances of bult-in layers.
  In addition to this way of layers instantiation, there is a more common factory API (see @ref dnnLayerFactory), it allows to create layers dynamically (by name) and register new ones.
  You can use both API, but factory API is less convinient for native C++ programming and basically designed for use inside importers (see @ref Importer, @ref createCaffeImporter(), @ref createTorchImporter()).

  Bult-in layers partially reproduce functionality of corresponding Caffe and Torch7 layers.
  In partuclar, the following layers and Caffe @ref Importer were tested to reproduce <a href="http://caffe.berkeleyvision.org/tutorial/layers.html">Caffe</a> functionality:
  - Convolution
  - Deconvolution
  - Pooling
  - InnerProduct
  - TanH, ReLU, Sigmoid, BNLL, Power, AbsVal
  - Softmax
  - Reshape, Flatten, Slice, Split
  - LRN
  - MVN
  - Dropout (since it does nothing on forward pass -))
*/

    class CV_EXPORTS BlankLayer : public Layer
    {
    public:
        static Ptr<BlankLayer> create(const LayerParams &params);
    };

    //! LSTM recurrent layer
    class CV_EXPORTS LSTMLayer : public Layer
    {
    public:
        /** Creates instance of LSTM layer */
        static Ptr<LSTMLayer> create(const LayerParams& params);

        /** Set trained weights for LSTM layer.
        LSTM behavior on each step is defined by current input, previous output, previous cell state and learned weights.

        Let @f$x_t@f$ be current input, @f$h_t@f$ be current output, @f$c_t@f$ be current state.
        Than current output and current cell state is computed as follows:
        @f{eqnarray*}{
        h_t &= o_t \odot tanh(c_t),               \\
        c_t &= f_t \odot c_{t-1} + i_t \odot g_t, \\
        @f}
        where @f$\odot@f$ is per-element multiply operation and @f$i_t, f_t, o_t, g_t@f$ is internal gates that are computed using learned wights.

        Gates are computed as follows:
        @f{eqnarray*}{
        i_t &= sigmoid&(W_{xi} x_t + W_{hi} h_{t-1} + b_i), \\
        f_t &= sigmoid&(W_{xf} x_t + W_{hf} h_{t-1} + b_f), \\
        o_t &= sigmoid&(W_{xo} x_t + W_{ho} h_{t-1} + b_o), \\
        g_t &= tanh   &(W_{xg} x_t + W_{hg} h_{t-1} + b_g), \\
        @f}
        where @f$W_{x?}@f$, @f$W_{h?}@f$ and @f$b_{?}@f$ are learned weights represented as matrices:
        @f$W_{x?} \in R^{N_h \times N_x}@f$, @f$W_{h?} \in R^{N_h \times N_h}@f$, @f$b_? \in R^{N_h}@f$.

        For simplicity and performance purposes we use @f$ W_x = [W_{xi}; W_{xf}; W_{xo}, W_{xg}] @f$
        (i.e. @f$W_x@f$ is vertical contacentaion of @f$ W_{x?} @f$), @f$ W_x \in R^{4N_h \times N_x} @f$.
        The same for @f$ W_h = [W_{hi}; W_{hf}; W_{ho}, W_{hg}], W_h \in R^{4N_h \times N_h} @f$
        and for @f$ b = [b_i; b_f, b_o, b_g]@f$, @f$b \in R^{4N_h} @f$.

        @param Wh is matrix defining how previous output is transformed to internal gates (i.e. according to abovemtioned notation is @f$ W_h @f$)
        @param Wx is matrix defining how current input is transformed to internal gates (i.e. according to abovemtioned notation is @f$ W_x @f$)
        @param b  is bias vector (i.e. according to abovemtioned notation is @f$ b @f$)
        */
        virtual void setWeights(const Mat &Wh, const Mat &Wx, const Mat &b) = 0;

        /** @brief Specifies shape of output blob which will be [[`T`], `N`] + @p outTailShape.
          * @details If this parameter is empty or unset then @p outTailShape = [`Wh`.size(0)] will be used,
          * where `Wh` is parameter from setWeights().
          */
        virtual void setOutShape(const MatShape &outTailShape = MatShape()) = 0;

        /** @brief Specifies either interpet first dimension of input blob as timestamp dimenion either as sample.
          *
          * If flag is set to true then shape of input blob will be interpeted as [`T`, `N`, `[data dims]`] where `T` specifies number of timpestamps, `N` is number of independent streams.
          * In this case each forward() call will iterate through `T` timestamps and update layer's state `T` times.
          *
          * If flag is set to false then shape of input blob will be interpeted as [`N`, `[data dims]`].
          * In this case each forward() call will make one iteration and produce one timestamp with shape [`N`, `[out dims]`].
          */
        virtual void setUseTimstampsDim(bool use = true) = 0;

        /** @brief If this flag is set to true then layer will produce @f$ c_t @f$ as second output.
         * @details Shape of the second output is the same as first output.
         */
        virtual void setProduceCellOutput(bool produce = false) = 0;

        /* In common case it use single input with @f$x_t@f$ values to compute output(s) @f$h_t@f$ (and @f$c_t@f$).
         * @param input should contain packed values @f$x_t@f$
         * @param output contains computed outputs: @f$h_t@f$ (and @f$c_t@f$ if setProduceCellOutput() flag was set to true).
         *
         * If setUseTimstampsDim() is set to true then @p input[0] should has at least two dimensions with the following shape: [`T`, `N`, `[data dims]`],
         * where `T` specifies number of timpestamps, `N` is number of independent streams (i.e. @f$ x_{t_0 + t}^{stream} @f$ is stored inside @p input[0][t, stream, ...]).
         *
         * If setUseTimstampsDim() is set to fase then @p input[0] should contain single timestamp, its shape should has form [`N`, `[data dims]`] with at least one dimension.
         * (i.e. @f$ x_{t}^{stream} @f$ is stored inside @p input[0][stream, ...]).
        */

        int inputNameToIndex(String inputName);
        int outputNameToIndex(String outputName);
    };

    /** @brief Classical recurrent layer

    Accepts two inputs @f$x_t@f$ and @f$h_{t-1}@f$ and compute two outputs @f$o_t@f$ and @f$h_t@f$.

    - input: should contain packed input @f$x_t@f$.
    - output: should contain output @f$o_t@f$ (and @f$h_t@f$ if setProduceHiddenOutput() is set to true).

    input[0] should have shape [`T`, `N`, `data_dims`] where `T` and `N` is number of timestamps and number of independent samples of @f$x_t@f$ respectively.

    output[0] will have shape [`T`, `N`, @f$N_o@f$], where @f$N_o@f$ is number of rows in @f$ W_{xo} @f$ matrix.

    If setProduceHiddenOutput() is set to true then @p output[1] will contain a Mat with shape [`T`, `N`, @f$N_h@f$], where @f$N_h@f$ is number of rows in @f$ W_{hh} @f$ matrix.
    */
    class CV_EXPORTS RNNLayer : public Layer
    {
    public:
        /** Creates instance of RNNLayer */
        static Ptr<RNNLayer> create(const LayerParams& params);

        /** Setups learned weights.

        Recurrent-layer behavior on each step is defined by current input @f$ x_t @f$, previous state @f$ h_t @f$ and learned weights as follows:
        @f{eqnarray*}{
        h_t &= tanh&(W_{hh} h_{t-1} + W_{xh} x_t + b_h),  \\
        o_t &= tanh&(W_{ho} h_t + b_o),
        @f}

        @param Wxh is @f$ W_{xh} @f$ matrix
        @param bh  is @f$ b_{h}  @f$ vector
        @param Whh is @f$ W_{hh} @f$ matrix
        @param Who is @f$ W_{xo} @f$ matrix
        @param bo  is @f$ b_{o}  @f$ vector
        */
        virtual void setWeights(const Mat &Wxh, const Mat &bh, const Mat &Whh, const Mat &Who, const Mat &bo) = 0;

        /** @brief If this flag is set to true then layer will produce @f$ h_t @f$ as second output.
         * @details Shape of the second output is the same as first output.
         */
        virtual void setProduceHiddenOutput(bool produce = false) = 0;

    };

    class CV_EXPORTS BaseConvolutionLayer : public Layer
    {
    public:
        Size kernel, stride, pad, dilation, adjustPad;
        String padMode;
    };

    class CV_EXPORTS ConvolutionLayer : public BaseConvolutionLayer
    {
    public:
        static Ptr<BaseConvolutionLayer> create(const LayerParams& params);
    };

    class CV_EXPORTS DeconvolutionLayer : public BaseConvolutionLayer
    {
    public:
        static Ptr<BaseConvolutionLayer> create(const LayerParams& params);
    };

    class CV_EXPORTS LRNLayer : public Layer
    {
    public:
        enum Type
        {
            CHANNEL_NRM,
            SPATIAL_NRM
        };
        int type;

        int size;
        float alpha, beta, bias;
        bool normBySize;

        static Ptr<LRNLayer> create(const LayerParams& params);
    };

    class CV_EXPORTS PoolingLayer : public Layer
    {
    public:
        enum Type
        {
            MAX,
            AVE,
            STOCHASTIC
        };

        int type;
        Size kernel, stride, pad;
        bool globalPooling;
        bool computeMaxIdx;
        String padMode;

        static Ptr<PoolingLayer> create(const LayerParams& params);
    };

    class CV_EXPORTS SoftmaxLayer : public Layer
    {
    public:
        bool logSoftMax;

        static Ptr<SoftmaxLayer> create(const LayerParams& params);
    };

    class CV_EXPORTS InnerProductLayer : public Layer
    {
    public:
        int axis;
        static Ptr<InnerProductLayer> create(const LayerParams& params);
    };

    class CV_EXPORTS MVNLayer : public Layer
    {
    public:
        float eps;
        bool normVariance, acrossChannels;

        static Ptr<MVNLayer> create(const LayerParams& params);
    };

    /* Reshaping */

    class CV_EXPORTS ReshapeLayer : public Layer
    {
    public:
        MatShape newShapeDesc;
        Range newShapeRange;

        static Ptr<ReshapeLayer> create(const LayerParams& params);
    };

    class CV_EXPORTS FlattenLayer : public Layer
    {
    public:
        static Ptr<FlattenLayer> create(const LayerParams &params);
    };

    class CV_EXPORTS ConcatLayer : public Layer
    {
    public:
        int axis;

        static Ptr<ConcatLayer> create(const LayerParams &params);
    };

    class CV_EXPORTS SplitLayer : public Layer
    {
    public:
        int outputsCount; //!< Number of copies that will be produced (is ignored when negative).

        static Ptr<SplitLayer> create(const LayerParams &params);
    };

    class CV_EXPORTS SliceLayer : public Layer
    {
    public:
        int axis;
        std::vector<int> sliceIndices;

        static Ptr<SliceLayer> create(const LayerParams &params);
    };

    class CV_EXPORTS PermuteLayer : public Layer
    {
    public:
        static Ptr<PermuteLayer> create(const LayerParams& params);
    };

    class CV_EXPORTS PaddingLayer : public Layer
    {
    public:
        static Ptr<PaddingLayer> create(const LayerParams& params);
    };

    /* Activations */
    class CV_EXPORTS ActivationLayer : public Layer
    {
    public:
        virtual void forwardSlice(const float* src, float* dst, int len,
                                  size_t outPlaneSize, int cn0, int cn1) const = 0;
    };

    class CV_EXPORTS ReLULayer : public ActivationLayer
    {
    public:
        float negativeSlope;

        static Ptr<ReLULayer> create(const LayerParams &params);
    };

    class CV_EXPORTS ChannelsPReLULayer : public ActivationLayer
    {
    public:
        static Ptr<ChannelsPReLULayer> create(const LayerParams& params);
    };

    class CV_EXPORTS ELULayer : public ActivationLayer
    {
    public:
        static Ptr<ELULayer> create(const LayerParams &params);
    };

    class CV_EXPORTS TanHLayer : public ActivationLayer
    {
    public:
        static Ptr<TanHLayer> create(const LayerParams &params);
    };

    class CV_EXPORTS SigmoidLayer : public ActivationLayer
    {
    public:
        static Ptr<SigmoidLayer> create(const LayerParams &params);
    };

    class CV_EXPORTS BNLLLayer : public ActivationLayer
    {
    public:
        static Ptr<BNLLLayer> create(const LayerParams &params);
    };

    class CV_EXPORTS AbsLayer : public ActivationLayer
    {
    public:
        static Ptr<AbsLayer> create(const LayerParams &params);
    };

    class CV_EXPORTS PowerLayer : public ActivationLayer
    {
    public:
        float power, scale, shift;

        static Ptr<PowerLayer> create(const LayerParams &params);
    };

    /* Layers used in semantic segmentation */

    class CV_EXPORTS CropLayer : public Layer
    {
    public:
        int startAxis;
        std::vector<int> offset;

        static Ptr<CropLayer> create(const LayerParams &params);
    };

    class CV_EXPORTS EltwiseLayer : public Layer
    {
    public:
        enum EltwiseOp
        {
            PROD = 0,
            SUM = 1,
            MAX = 2,
        };

        static Ptr<EltwiseLayer> create(const LayerParams &params);
    };

    class CV_EXPORTS BatchNormLayer : public Layer
    {
    public:
        bool hasWeights, hasBias;
        float epsilon;

        virtual void getScaleShift(Mat& scale, Mat& shift) const = 0;
        static Ptr<BatchNormLayer> create(const LayerParams &params);
    };

    class CV_EXPORTS MaxUnpoolLayer : public Layer
    {
    public:
        Size poolKernel;
        Size poolPad;
        Size poolStride;

        static Ptr<MaxUnpoolLayer> create(const LayerParams &params);
    };

    class CV_EXPORTS ScaleLayer : public Layer
    {
    public:
        bool hasBias;

        static Ptr<ScaleLayer> create(const LayerParams& params);
    };

    class CV_EXPORTS ShiftLayer : public Layer
    {
    public:
        static Ptr<ShiftLayer> create(const LayerParams& params);
    };

    class CV_EXPORTS PriorBoxLayer : public Layer
    {
    public:
        static Ptr<PriorBoxLayer> create(const LayerParams& params);
    };

    class CV_EXPORTS DetectionOutputLayer : public Layer
    {
    public:
        static Ptr<DetectionOutputLayer> create(const LayerParams& params);
    };

    class NormalizeBBoxLayer : public Layer
    {
    public:
        static Ptr<NormalizeBBoxLayer> create(const LayerParams& params);
    };

//! @}
//! @}
CV__DNN_EXPERIMENTAL_NS_END
}
}
#endif
