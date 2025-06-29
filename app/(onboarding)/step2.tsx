import React from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import LottieLoader from "../../components/LottieLoader";
import { router } from "expo-router";

export default function OnboardingStep2() {
  return (
    <View style={styles.container}>
      <LottieLoader source={require("../../assets/lottie/onboarding2.json")} />
      <Text style={styles.title}>Daily Check-Ins</Text>
      <Text style={styles.text}>
        Every day is a new journey. Use our daily check-ins to track your mood
        and reflect on your feelings. This habit builds self-awareness and helps
        you notice your progress over time.
      </Text>
      <Button
        title="Next"
        color="#388E3C"
        onPress={() => router.push("/(onboarding)/step3")}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#B6E2D3", // Pastel green
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#388E3C",
    marginBottom: 20,
  },
  text: {
    fontSize: 18,
    color: "#2D3A4A",
    textAlign: "center",
    marginBottom: 40,
  },
});
