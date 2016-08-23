/**
   @author Kunio Kojima
*/
#pragma once

#include <iostream>
#include <sstream>
#include <fstream>
#include <map>

#include <time.h>

#include <boost/bind.hpp>

#include <cnoid/Plugin>
#include <cnoid/ItemTreeView>
#include <cnoid/BodyItem>
#include <cnoid/MessageView>
#include <cnoid/src/PoseSeqPlugin/PoseSeqItem.h>
#include <cnoid/src/PoseSeqPlugin/BodyMotionGenerationBar.h>
#include <cnoid/FileUtil>

#include <UtilPlugin/UtilPlugin.h>

#include "SlideFrictionControl.h"
#include "SlideFrictionControlBar.h"

namespace cnoid{
    void generatePreModelPredictiveControlParamDeque(hrp::SlideFrictionControl* sfc, BodyPtr body, const PoseSeqPtr poseSeqPtr, const BodyMotionPtr& motion, const std::set<Link*>& contactLinkCandidateSet);
    void generateContactConstraintParamVec2(std::vector<hrp::ContactConstraintParam*>& ccParamVec, const std::set<Link*>& contactLinkCandidateSet, PoseSeq::iterator poseIter, const PoseSeqPtr& poseSeqPtr);
    void generateSlideFrictionControlParam(hrp::SlideFrictionControlParam* sfcParam, Vector3d& lastP, BodyPtr body, std::vector<hrp::ContactConstraintParam*>& ccParamVec, double dt);
    void sweepControl(std::ofstream& ofs, hrp::SlideFrictionControl* sfc, BodyPtr& body, BodyMotionItemPtr& bodyMotionItemPtr);

    class SlideFrictionControlBar;

    class SlideFrictionControlPlugin : public Plugin
    {
    private:
        Vector3SeqPtr mRefCMSeqPtr, mRefPSeqPtr, mRefLSeqPtr;
        std::ofstream mOfs;
        hrp::SlideFrictionControl* sfc;
        Vector3d lastP;
        std::vector<int> failIdxVec;

    public:
        BodyPtr body;
        BodyMotionItemPtr mBodyMotionItemPtr;
        BodyMotionPtr motion;
        SlideFrictionControlBar* mBar;

        boost::filesystem::path mPoseSeqPath;

        int frameRate;
        double dt;
        int numFrames;

        SlideFrictionControlPlugin() : Plugin("SlideFrictionControl")
        {
            require("Body");
            require("PoseSeq");
            // require("Dynamics");
        }
    
        virtual bool initialize();
        void execControl();

    };

}